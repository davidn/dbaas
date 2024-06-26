#!/usr/bin/python
from __future__ import unicode_literals
import re
from logging import getLogger
from time import sleep
from django.conf import settings
from .cloud import Cloud
from ..exceptions import LaunchException
from api.utils import retry

import boto.ec2
from boto.exception import EC2ResponseError

logger = getLogger(__name__)


class EC2(Cloud):
    @property
    def ec2(self):
        if not hasattr(self, '_ec2'):
            self._ec2 = boto.ec2.get_region(self.region.code).connect(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                                                      aws_secret_access_key=settings.AWS_SECRET_KEY)
        return self._ec2

    def __getstate__(self):
        if hasattr(self, '_ec2'):
            odict = self.__dict__.copy()
            del odict['_ec2']
            return odict
        else:
            return self.__dict__

    @staticmethod
    def null_or_io1(iops):
        if iops is None:
            return None
        else:
            return 'io1'

    def _create_security_group(self, node, security_group):
        try:
            sg = self.ec2.create_security_group(security_group, 'Security group for ' + security_group)
        except EC2ResponseError, e:
            if re.search('InvalidGroup.Duplicate', e.body) is None:
                raise
            sg = self.ec2.get_all_security_groups([str(node)])[0]
        node.security_group = sg.id

        try:
            self.ec2.authorize_security_group(
                group_id=sg.id,
                ip_protocol='tcp',
                cidr_ip='0.0.0.0/0',
                from_port=node.cluster.port,
                to_port=node.cluster.port)
        except EC2ResponseError, e:
            if re.search('InvalidPermission.Duplicate', e.body) is None:
                raise

        logger.debug("%s: Created Security Group %s (named %s) with port %s open", node, sg.id, sg.name,
                     node.cluster.port)
        node.save()
        return sg

    def _create_block_device_map(self, node):
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = boto.ec2.blockdevicemapping.BlockDeviceType(
            iops=node.iops,
            volume_type=self.null_or_io1(node.iops),
            delete_on_termination=True
        )
        if node.storage is None:
            for i in xrange(node.flavor.fixed_storage_volumes):
                bdm['/dev/sd%s' % chr(ord('b')+i)] = boto.ec2.blockdevicemapping.BlockDeviceType(
                    ephemeral_name='ephemeral%d' % i)
        else:
            bdm['/dev/sdf'] = boto.ec2.blockdevicemapping.BlockDeviceType(
                iops=node.iops,
                volume_type=self.null_or_io1(node.iops),
                delete_on_termination=True,
                size=node.storage
            )
        return bdm

    def _run_instances(self, node, sgs):
        last_exc = None
        zones = sorted(z.name for z in self.ec2.get_all_zones())
        # each nodes try different zones first.
        zones = zones[node.nid % len(zones):] + zones[:node.nid % len(zones)]
        for zone in zones:
            try:
                return self.ec2.run_instances(
                    self.region.image,
                    key_name=self.region.key_name,
                    instance_type=node.flavor.code,
                    block_device_map=self._create_block_device_map(node),
                    security_groups=sgs,
                    user_data=self.cloud_init(node),
                    placement=zone,
                )
            except EC2ResponseError as e:
                last_exc = e
        if last_exc is None:
            raise LaunchException("No zones available to attempt launch in.")
        raise last_exc

    def launch(self, node):
        logger.debug("%s: Assigned NID %s", node, node.nid)
        sg = retry(lambda: self._create_security_group(node, str(node)))
        # EC2 Instance
        if self.region.security_group == "":
            sgs = [sg.name]
        else:
            sgs = [sg.name, self.region.security_group]

        def ec2_run_instances():
            return self._run_instances(node, sgs)

        try:
            res = retry(ec2_run_instances)
        except:
            logger.error("run_instances failed, deleting security group. Node: %s", node)

            def ec2_delete_security():
                return self.ec2.delete_security_group(group_id=node.security_group)
            try:
                retry(ec2_delete_security)
            except:
                logger.error("delete_security_group failed, Node:%s", node)
                #TODO Better manage failures
            raise

        node.instance_id = res.instances[0].id
        logger.debug("%s: Reservation %s launched. Instance id %s", node, res.id, node.instance_id)

    def pending(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'pending'

    def shutting_down(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'shutting-down'

    def reinstantiating(self, node):
        return self.pending(node)

    def get_ip(self, node):
        instance = self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0]
        return instance.ip_address

    def update(self, node, tags=None):
        if tags is None:
            tags = dict()
        instance = self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0]
        for k, v in tags.items():
            instance.add_tag(k, v)

    def terminate(self, node):
        if node.security_group != "":
            if node.instance_id != "":
                try:
                    self.ec2.terminate_instances([node.instance_id])
                    while node.shutting_down():
                        sleep(15)
                except EC2ResponseError, e:
                    if re.search('InvalidInstanceID.NotFound', e.body) is None:
                        raise
            logger.debug("%s: terminating security group %s", node, node.security_group)
            try:
                self.ec2.delete_security_group(group_id=node.security_group)
            except EC2ResponseError:
                logger.error("%s: failed to terminate security group %s", node, node.security_group, exc_info=True)

    def reinstantiate_setup(self, node):
        # Note: this command stops the server and then restarts it as a new instance
        self.ec2.stop_instances([node.instance_id])
        while self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'stopping':
            sleep(15)
        self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].modify_attribute('instanceType',
                                                                                                     node.flavor.code)

    def reinstantiate(self, node):
        try:
            self.ec2.start_instances([node.instance_id])
        except:
            logger.error("resizing attempt to %s failed, Node:%s", node.flavor.code, node.dns_name)
            raise
        logger.info("Reinstantiating the AWS Instance %s", node.dns_name)
