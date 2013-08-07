from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
import boto.ec2
import novaclient.v1_1

logger = getLogger(__name__)

class Cloud(object):
    def __init__(self, region):
        self.region = region
    def launch(self, node):
        pass
    def pending(self, node):
        pass
    def shutting_down(self, node):
        pass
    def update(self, node, tags={}):
        pass
    def terminate(self, node):
        pass
    def pause(self, node):
        pass
    def resume(self, node):
        pass

class EC2(Cloud):
    @property
    def ec2(self):
        if not hasattr(self, '_ec2'):
            self._ec2 = boto.ec2.get_region(self.region.code).connect(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        return self._ec2

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['_ec2']
        return odict

    def null_or_io1(self, iops):
        if iops is None:
            return None
        else:
            return 'io1'

    def launch(self, node):
        # Elastic Block Storage
        dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType(iops=node.iops, volume_type=self.null_or_io1(node.iops))
        dev_sda1.size = node.storage
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1
        logger.debug("%s: Assigned NID %s", node, node.nid)
        sg = self.ec2.create_security_group(str(node),'Security group for '+str(node))
        node.security_group = sg.id
        self.ec2.authorize_security_group(
            group_id=sg.id,
            ip_protocol='tcp',
            cidr_ip='0.0.0.0/0',
            from_port=node.cluster.port,
            to_port=node.cluster.port)
        logger.debug("%s: Created Security Group %s (named %s) with port %s open", node, sg.id, sg.name, node.cluster.port)
        node.save()
        # EC2 Instance
        if self.region.security_group == "":
            sgs = [sg.name]
        else:
            sgs = [sg.name, self.region.security_group]
        try:
            res = self.ec2.run_instances(
                self.region.image,
                key_name=self.region.key_name,
                instance_type=node.flavor.code,
                block_device_map=bdm,
                security_groups=sgs,
                user_data ='#include\nhttps://'+Site.objects.get_current().domain+node.get_absolute_url()+'cloud_config/',
            )
        except:
            try:
                self.ec2.delete_security_group(group_id=node.security_group)
            except:
                pass
            raise
        node.instance_id = res.instances[0].id
        logger.debug("%s: Reservation %s launched. Instance id %s", node, res.id, node.instance_id)
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'pending'

    def shutting_down(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'shutting-down'

    def update(self, node, tags={}):
        instance = self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0]
        node.ip = instance.ip_address
        node.save()
        for k,v in tags.items():
            instance.add_tag(k, v)

    def terminate(self, node):
        self.ec2.terminate_instances([node.instance_id])
        if node.security_group != "":
            node.status = node.SHUTTING_DOWN
            node.save()
            while node.shutting_down():
                sleep(15)
            logger.debug("%s: terminating security group %s", node, node.security_group)
            self.ec2.delete_security_group(group_id=node.security_group)

    def pause(self, node):
        self.ec2.stop_instances([node.instance_id])

    def resume(self, node):
        self.ec2.start_instances([node.instance_id])

class Openstack(Cloud):
    @property
    def nova(self):
        if not hasattr(self, "_nova"):
            self._nova = novaclient.v1_1.client.Client(self.USER,
                self.PASS,
                self.TENANT,
                self.AUTH_URL,
                service_type="compute",
                region_name=self.region.code)
        return self._nova

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['_nova']
        return odict

    def launch(self, node):
        server = self.nova.servers.create(
            name= node.dns_name,
            image=self.region.image,
            flavor=node.flavor.code,
            key_name=self.region.key_name,
            availability_zone=self.region.code,
            files={
                '/var/lib/cloud/seed/nocloud/user-data':'#include\nhttps://'+Site.objects.get_current().domain+node.get_absolute_url()+'cloud_config/',
                '/var/lib/cloud/seed/nocloud/meta-data':'',
            },
        )
        node.instance_id = server.id
        node.status=node.PROVISIONING

    def pending(self, node):
        return self.nova.servers.get(node.instance_id).status == u'BUILD'

    def shutting_down(self, node):
        return self.nova.servers.get(node.instance_id).status == u'STOPPING'

    def update(self, node, tags=None):
        if tags is None:
            tags = {}
        tags['id'] = node.instance_id
        s = self.nova.servers.set_meta(node.instance_id, tags)
        node.ip = s.accessIPv4
        node.save()

    def terminate(self, node):
        self.nova.servers.delete(node.instance_id)

    def pause(self, node):
        self.nova.servers.suspend(node.instance_id)

    def resume(self, node):
        self.nova.servers.resume(node.instance_id)

class Rackspace(Openstack):
    USER = settings.RACKSPACE_USER
    PASS = settings.RACKSPACE_PASS
    TENANT = settings.RACKSPACE_TENANT
    AUTH_URL = settings.RACKSPACE_AUTH_URL