from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
import httplib2

try:
    from apiclient import discovery
    from oauth2client import client
except:
    pass

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

        _retryEC2(ec2_authorize_security_group)
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

        res = _retryEC2(ec2_run_instances)
        if not res:
            logger.error("run_instances failed, deleting security group. Node: %s", node)

            def ec2_delete_security():
                return self.ec2.delete_security_group(group_id=node.security_group)

            res = _retryEC2(ec2_delete_security)
            if not res:
                logger.error("delete_security_group failed, Node:%s", node)
                #TODO Better manage failures
            raise Exception("ec2_run_instances failed")

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


def _retryEC2(func, initialDelay=50, maxRetries=12):
    delay = initialDelay
    for retry in range(maxRetries):
        try:
            result = func()
            if result:
                break
            sleep(delay / 1000.0)
        except:
            #Logging for this can be captured from Boto
            pass
        delay *= 2
    else:
        logger.error("Giving up on EC2 after %d attempts", maxRetries)

    return result


class GoogleComputeEngine(Cloud):
    SERVICE_PROJECT_ID  = settings.GCE_PROJECT_ID
    SERVICE_ACCT_EMAIL  = settings.GCE_SERVICE_ACCOUNT_EMAIL
    SERVICE_PRIVATE_KEY = settings.GCE_PRIVATE_KEY

    MAX_DELAY_RETRIES   = 40        # Max delay of 200 seconds
    RETRY_DELAY         = 5
    @property
    def gce(self):
        if not hasattr(self, "_gce_params"):
            credentials = client.SignedJwtAssertionCredentials(
              service_account_name=GoogleComputeEngine.SERVICE_ACCT_EMAIL,
              private_key=GoogleComputeEngine.SERVICE_PRIVATE_KEY,
              scope=[
                'https://www.googleapis.com/auth/compute',
                'https://www.googleapis.com/auth/devstorage.full_control',
                'https://www.googleapis.com/auth/devstorage.read_write',
              ])
            # Create an httplib2.Http object to handle our HTTP requests and authorize it
            # with our good Credentials.
            http = httplib2.Http()
            auth_http = credentials.authorize(http)
            # Construct the service object for the interacting with the Compute Engine API.
            gce_service = discovery.build('compute', 'v1beta16', http=auth_http)
            self._gce_params = {
                'credentials':credentials,
                'auth_http':auth_http,
                'service':gce_service,
                'project':GoogleComputeEngine.SERVICE_PROJECT_ID,
                'zone':'',
                'name':'',
                'nid':None,
                'machineType':'',
                'kernel':'google/global/kernels/gce-v20130813',
                'imageType':'',
                'imageName':'',
                'ip':'' }
        return self._gce_params

    def __getstate__(self):
        if hasattr(self, '_gce_params'):
            odict = self.__dict__.copy()
            del odict['_gce_params']
            return odict
        else:
            return self.__dict__

    @property
    def instance_name(self):
        if self.gce['name']:
            return self.gce['name']
        return None

    def filterNames(self, items, matchNames=None):
        if matchNames is not None:
            allItems = items
            items = []
            if type(matchNames) == type(''):
                matchNames = [matchNames]
            for item in allItems:
                if item['name'] in matchNames:
                    items.append(item)
        return items

    def getInstanceObjects(self, matchNames=None):
        # Fetch the instance
        request = self.gce['service'].instances().list(project=self.gce['project'], zone=self.gce['zone'])
        response = request.execute()
        try:
            items = response['items']
        except:
            items = []
        return self.filterNames(items, matchNames)

    def getDiskObjects(self, matchNames=None):
        # Fetch the instance
        request = self.gce['service'].disks().list(project=self.gce['project'], zone=self.gce['zone'])
        response = request.execute()
        try:
            items = response['items']
        except:
            items = []
        return self.filterNames(items, matchNames)

    def launch(self, node):
        self.gce['zone'] = self.region.name
        self.gce['name'] = make_gce_valid_name('dbaas-cluster-{c}-node-{n}'.format(c=node.cluster.pk, n=node.nid))
        self.gce['nid'] = node.nid
        self.gce['machineType'] = node.flavor.name
        self.gce['imageName'] = 'dbaas-test'
        logger.debug("%(name)s: Assigned NID %(nid)s" % self.gce)

        #
        # Create a persistent Disk for the Instance to mount
        #
        body = {
          "name": self.gce['name'],
          "sizeGb": node.storage,
          "description": "boot disk",
          "sourceImage": 'https://www.googleapis.com/compute/v1beta16/projects/%(project)s/global/images/%(imageName)s' % self.gce,
        }
        request = self.gce['service'].disks().insert(project=self.gce['project'], body=body, zone=self.gce['zone'])
        response = request.execute(self.gce['auth_http'])

        sleep(2)
        for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
            disks = self.getDiskObjects(self.gce['name'])
            if disks:
                break
            sleep(GoogleComputeEngine.RETRY_DELAY)

        #
        # Create the Instance
        #
        # Construct the request body
        disk_body = [
          {'source': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/disks/%(name)s" % self.gce,
           'boot': True,
           'type': 'PERSISTENT',
           'mode': 'READ_WRITE',
           'deviceName': "bootdisk",
          }]
        netIfc_body = [{
            'accessConfigs': [{
              'type': 'ONE_TO_ONE_NAT',
              'name': 'External NAT'
             }],
            'network': 'https://www.googleapis.com/compute/v1beta16/projects/%(project)s/global/networks/default' % self.gce,
          }]
        body = {
          'name': self.gce['name'],
          'kernel': 'https://www.googleapis.com/compute/v1beta16/projects/%(kernel)s' % self.gce,
          'machineType': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/machineTypes/%(machineType)s" % self.gce,
          'networkInterfaces': netIfc_body,
          'disks': disk_body,
          'description': '%(name)s instance' % self.gce,
          'metadata': {'items': [], 'kind': 'compute#metadata'}
        }

        # Create the instance
        request = self.gce['service'].instances().insert(project=self.gce['project'], body=body, zone=self.gce['zone'])
        response = request.execute(self.gce['auth_http'])
        logger.info("Created the GCE Instance %(name)s" % (self.gce))
        node.instance_id = self.gce['name']
        node.security_group = self.gce['zone']
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        items = self.getInstanceObjects(self.gce['name'])
        if items:
            try:
                self.gce['ip'] = items[0]['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            except:
                pass
        if items and items[0]['status'] == 'RUNNING':
            return False
        return True

    def shutting_down(self, node):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        items = self.getInstanceObjects(self.gce['name'])
        return items != []

    def update(self, node, tags=None):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group

        updateProperties = []   # Put in the list of supported metadata properties when they are known.
        body = {"items": []}
        if tags is None:
            tags = {}
        for k in tags.keys():
            if k not in updateProperties:
                del tags[k]
        if tags:
            body['items'].append( {"name": node.instance_id} )  # Is this the right property name?
            for k, v in tags.items():
                body['items'].append( {k: v} )
            request = self.gce['service'].instances().setMetadata(project=self.gce['project'], zone=self.gce['zone'], instance=self.gce['name'], body=body)
            response = request.execute(self.gce['auth_http'])

        items = self.getInstanceObjects(self.gce['name'])
        if items:
            try:
                self.gce['ip'] = items[0]['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            except:
                pass
        node.ip = self.gce['ip']
        node.save()

    def terminate(self, node):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        if node.instance_id != "":
            self.gce['name'] = node.instance_id
            if node.status != node.SHUTTING_DOWN:
                node.status = node.SHUTTING_DOWN
                node.save()
            #
            # Delete the instance
            #
            request = self.gce['service'].instances().delete(project=self.gce['project'], zone=self.gce['zone'], instance=self.gce['name'])
            response = request.execute(self.gce['auth_http'])
            logger.debug("Terminating GCE Instance %(name)s" % self.gce)
            #
            # Wait for Shutdown to occur.
            #
            for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
                if not node.shutting_down():
                    break
                sleep(GoogleComputeEngine.RETRY_DELAY)
            #
            # We also need to delete the persistent disk.
            #
            request = self.gce['service'].disks().delete(project=self.gce['project'], zone=self.gce['zone'], disk=self.gce['name'])
            response = request.execute(self.gce['auth_http'])
            node.instance_id = ""

    #def pause(self, node):
    #    # Note: this command halts, doesn't suspend, the server
    #    self.gce['name'] = node.instance_id
    #    self.gce['zone'] = node.security_group
    #    self.pb.stopServer(node.instance_id)

    #def resume(self, node):
    #    self.gce['name'] = node.instance_id
    #    self.gce['zone'] = node.security_group
    #    self.pb.startServer(node.instance_id)


def make_gce_valid_name(name):
    MAX_VALID_NAME_LEN  = 63    # GCE Instance Names must be <= this length
    FIRST_ALPHA         = "g"   # GCE Name must start with an alpha char
    if name[:1].isalpha():
        FIRST_ALPHA = ""
    i = name.find('.')
    if i >= MAX_VALID_NAME_LEN - len(FIRST_ALPHA):
        # If we can, drop the chars just before the Node ID
        k = name.rfind('-', 0, i)
        if k + MAX_VALID_NAME_LEN >= i + len(FIRST_ALPHA):
            j = k + MAX_VALID_NAME_LEN - i - len(FIRST_ALPHA)
            name = "".join((FIRST_ALPHA, name[:j], name[k:i]))
        else:
            name = FIRST_ALPHA + name[:MAX_VALID_NAME_LEN-1]
    elif (FIRST_ALPHA and name[:len(FIRST_ALPHA)] != FIRST_ALPHA) or i >= 0:
        name = FIRST_ALPHA + name[:i]
    elif len(name) > MAX_VALID_NAME_LEN:
        name = name[:MAX_VALID_NAME_LEN]
    return name.lower()


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
        logger.debug("%s: Assigned NID %s" % (str(node), node.nid))

        # Create the Data Center
        logger.debug("Creating the DataCenter - %s, %s" % (self.region.name, str(self.region.code)))
        dcId = self.pb.createDataCenter(str(node), self.region.code).dataCenterId
        res = _PBwait4avail(dcId, self.pb.getDataCenter)
        if not res:
            logger.error("createDataCenter failed, Node:%s", node)
            #TODO Better manage failures
            raise Exception("pb_run_instances failed")

        # Create the Server
        logger.debug("Creating the Server - name=%s, cores=%d, ram=%d, dcId=%s" % (str(node), node.flavor.cpus, node.flavor.ram, str(dcId)))
        createServerRequest = {
            'serverName': str(node),
            'cores': node.flavor.cpus,
            'ram': node.flavor.ram,
            #'bootFromImageId': "",
            #'bootFromStorageId': "",
            'dataCenterId': dcId,
            #'availabilityZone': self.region.code,
            #'image': node.region.image,
            #    '/var/lib/cloud/seed/nocloud-net/user-data': '#include\nhttps://' + Site.objects.get_current().domain + node.get_absolute_url() + 'cloud_config/\n',
            #    '/var/lib/cloud/seed/nocloud-net/meta-data': 'instance-id: iid-local01',
            'internetAccess': True}
        svrId = self.pb.createServer(createServerRequest).serverId
        #res = _PBwait4avail(svrId, self.pb.getServer, initialDelay=250, maxRetries=12)
        #if not res:
        #    logger.error("createServer failed, Node:%s", node)
        #    #TODO Better manage failures
        #    raise Exception("pb_run_instances failed")

        # Create the Storage
        logger.debug("Creating the Storage - size=%d" % (node.storage))
        # Find the image object
        imageId = None
        images = self.pb.getAllImages()
        for image in images:
            if image['imageName'] == self.region.image:
                imageId = image['imageId']
                break
        logger.debug("mounting image=%s, Id=%s" % (self.region.image, str(imageId)))
        createStorageRequest = {
            'size': node.storage,
            'dataCenterId': dcId,
            'mountImageId': imageId,
            'storageName': str(node)}
        stgId = self.pb.createStorage(createStorageRequest).storageId
        #res = _PBwait4avail(stgId, self.pb.getStorage)
        #if not res:
        #    logger.error("createStorage failed, Node:%s", node)
        #    #TODO Better manage failures
        #    raise Exception("pb_run_instances failed")


        # Connect the Server to the Storage
        self.pb.connectStorageToServer({"storageId": stgId, "serverId": svrId})
        logger.debug("Connected the Storage to the Server - stgId=%s, svrId=%s" % (str(stgId), str(svrId)))

        node.security_group = dcId
        node.instance_id = svrId
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        svr = self.pb.getServer(node.instance_id)
        if svr and svr.provisioningState == 'AVAILABLE':
            return False
        return True

    def shutting_down(self, node):
        try:
            self.pb.getDataCenter(node.security_group)
            dcExists = True
        except:
            dcExists = False
        return dcExists

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

def _PBwait4avail(objid, getfunc, objField='provisioningState', targetValues=['AVAILABLE'], initialDelay=50, maxRetries=12):
    result = None
    delay = initialDelay
    for retry in range(maxRetries):
        try:
            obj = getfunc(objid)
            state = getattr(obj, objField)
            if state in targetValues:
                result = obj
                break
            sleep(delay / 1000.0)
        except:
            #Logging for this can be captured from the obj data
            pass
        delay *= 2
    else:
        logger.error("Giving up on PB after %d attempts", maxRetries)
    return result


