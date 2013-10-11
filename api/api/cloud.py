from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
from .utils import retry

try:
    import pb.client
except:
    pass

import boto.ec2
import novaclient.v1_1

logger = getLogger(__name__)


def remove_trail_slash(s):
    if s.endswith('/'):
        s = s[:-1]
    return s


class Cloud(object):
    def __init__(self, region):
        self.region = region

    def launch(self, node):
        pass

    def pending(self, node):
        pass

    def shutting_down(self, node):
        pass

    def pausing(self, node):
        pass

    def resuming(self, node):
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

    def null_or_io1(self, iops):
        if iops is None:
            return None
        else:
            return 'io1'

    def _create_security_group(self, node):
        sg = self.ec2.create_security_group(str(node), 'Security group for ' + str(node))
        node.security_group = sg.id

        def ec2_authorize_security_group():
            self.ec2.authorize_security_group(
                group_id=sg.id,
                ip_protocol='tcp',
                cidr_ip='0.0.0.0/0',
                from_port=node.cluster.port,
                to_port=node.cluster.port)
            return True

        retry(ec2_authorize_security_group)
        logger.debug("%s: Created Security Group %s (named %s) with port %s open", node, sg.id, sg.name, node.cluster.port)
        node.save()
        return sg

    def _create_block_device_map(self, node):
        dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType(
            iops=node.iops,
            volume_type=self.null_or_io1(node.iops),
            delete_on_termination=True
        )
        dev_sda1.size = node.storage
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1
        return bdm

    def launch(self, node):
        logger.debug("%s: Assigned NID %s", node, node.nid)
        sg = self._create_security_group(node)
        # EC2 Instance
        if self.region.security_group == "":
            sgs = [sg.name]
        else:
            sgs = [sg.name, self.region.security_group]


        def ec2_run_instances():
            return self.ec2.run_instances(
                self.region.image,
                key_name=self.region.key_name,
                instance_type=node.flavor.code,
                block_device_map=self._create_block_device_map(node),
                security_groups=sgs,
                user_data='#include\nhttps://' + Site.objects.get_current().domain + remove_trail_slash(
                    node.get_absolute_url()) + '/cloud_config/\n',
            )

        try:
            res = retry(ec2_run_instances)
        except:
            logger.error("run_instances failed, deleting security group. Node: %s", node)
            def ec2_delete_security():
                return self.ec2.delete_security_group(group_id=node.security_group)
            try:
                res = retry(ec2_delete_security)
            except:
                logger.error("delete_security_group failed, Node:%s", node)
                #TODO Better manage failures
            raise

        node.instance_id = res.instances[0].id
        logger.debug("%s: Reservation %s launched. Instance id %s", node, res.id, node.instance_id)
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'pending'

    def shutting_down(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'shutting-down'

    def pausing(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'stopping'

    def resuming(self, node):
        return self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0].update() == 'pending'

    def update(self, node, tags={}):
        instance = self.ec2.get_all_instances(instance_ids=[node.instance_id])[0].instances[0]
        node.ip = instance.ip_address
        node.save()
        for k, v in tags.items():
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
        if hasattr(self, '_nova'):
            odict = self.__dict__.copy()
            del odict['_nova']
            return odict
        else:
            return self.__dict__

    def launch(self, node):
        server = self.nova.servers.create(
            name=node.dns_name,
            image=self.region.image,
            flavor=node.flavor.code,
            key_name=self.region.key_name,
            availability_zone=self.region.code,
            files={
                '/var/lib/cloud/seed/nocloud-net/user-data': '#include\nhttps://' + Site.objects.get_current().domain + remove_trail_slash(node.get_absolute_url()) + '/cloud_config/\n',
                '/var/lib/cloud/seed/nocloud-net/meta-data': 'instance-id: iid-local01',
            },
        )
        node.instance_id = server.id
        node.status = node.PROVISIONING

    def pending(self, node):
        return self.nova.servers.get(node.instance_id).status == u'BUILD'

    def shutting_down(self, node):
        return self.nova.servers.get(node.instance_id).status == u'STOPPING'

    def pausing(self, node):
        return False

    def resuming(self, node):
        return False

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


class ProfitBrick(Cloud):
    USER = settings.PROFITBRICK_USER
    PASS = settings.PROFITBRICK_PASS

    @property
    def pb(self):
        if not hasattr(self, "_profitbrick"):
            self._profitbrick = pb.client.ClientProxy(ProfitBrick.USER, ProfitBrick.PASS, False)
        return self._profitbrick

    def __getstate__(self):
        if hasattr(self, '_profitbrick'):
            odict = self.__dict__.copy()
            del odict['_profitbrick']
            return odict
        else:
            return self.__dict__

    def launch(self, node):
        logger.debug("%s: Assigned NID %s", node, node.nid)

        # Create the Data Center
        logger.debug("Creating the DataCenter - %s, %s" % (self.region.name, str(self.region.code)))
        dcId = self.pb.createDataCenter(str(node), self.region.code).dataCenterId
        retry(lambda: provisioningStateAvailable(self.pb.getDataCenter(dcId)))

        # Create the Server
        logger.debug("Creating the Server - name=%s, cores=%d, ram=%d, dcId=%s" % (str(node), node.flavor.cpus, node.flavor.ram, str(dcId)))
        createServerRequest = {
            'serverName': str(node),
            'cores': node.flavor.cpus,
            'ram': node.flavor.ram,
            'dataCenterId': dcId,
            #'availabilityZone': self.region.code,
            #'image': node.region.image,
            #    '/var/lib/cloud/seed/nocloud-net/user-data': '#include\nhttps://' + Site.objects.get_current().domain + node.get_absolute_url() + 'cloud_config/\n',
            #    '/var/lib/cloud/seed/nocloud-net/meta-data': 'instance-id: iid-local01',
            'internetAccess': True}
        svrId = self.pb.createServer(createServerRequest).serverId
        retry(lambda: provisioningStateAvailable(self.pb.getServer(srvId)), initialDelay=250)

        # Create the Storage
        logger.debug("Creating the Storage - size=%d" % (node.storage))
        createStorageRequest = {
            'size': node.storage,
            'dataCenterId': dcId,
            'storageName': str(node)}
        #            'mountImageId': }
        stgId = self.pb.createStorage(createStorageRequest).storageId
        retry(lambda: provisioningStateAvailable(self.pb.getStorage(stgId)))

        # Connect the Server to the Storage
        self.pb.connectStorageToServer({"storageId": stgId, "serverId": svrId})
        logger.debug("Connected the Storage to the Server - stgId=%s, svrId=%s" % (str(stgId), str(svrId)))

        node.security_group = dcId
        node.instance_id = svrId
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        return self.pb.getServer(node.instance_id).provisioningState != 'AVAILABLE'

    def shutting_down(self, node):
        try:
            self.pb.getDataCenter(node.security_group)
            dcExists = True
        except:
            dcExists = False
        return dcExists

    def pausing(self, node):
        return False

    def resuming(self, node):
        return False

    def update(self, node, tags=None):
        updateProperties = ['serverName', 'cores', 'ram', 'bootFromImageId', 'availabilityZone', 'bootFromStorageId', 'osType']
        if tags is None:
            tags = {}
        for k in tags.keys():
            if k not in updateProperties:
                del tags[k]
        if tags:
            tags['serverId'] = node.instance_id
            logger.debug("PB.update: tags=%s" % (str(tags)))
            self.pb.updateServer(tags)
        s = self.pb.getServer(node.instance_id)
        node.ip = s.ips[0]
        node.save()

    def terminate(self, node):
        if node.instance_id != "":
            if node.status != node.SHUTTING_DOWN:
                node.status = node.SHUTTING_DOWN
                node.save()
            logger.debug("%s: terminating server %s", node, node.instance_id)
            self.pb.deleteServer(node.instance_id)
            node.instance_id = ""
        if node.security_group != "":
            if node.status != node.SHUTTING_DOWN:
                node.status = node.SHUTTING_DOWN
                node.save()
            self.pb.deleteDataCenter(node.security_group)
            logger.debug("%s: terminating security group %s", node, node.security_group)
            node.security_group = ""
        while node.shutting_down():
            sleep(15)

            #def pause(self, node):
            #    # Note: this command halts, doesn't suspend, the server
            #    self.pb.stopServer(node.instance_id)

            #def resume(self, node):
            #    self.pb.startServer(node.instance_id)

def provisioningStateAvailable(obj):
    if obj.provisioningState=='AVAILABLE':
        return object
