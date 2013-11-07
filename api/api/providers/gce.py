#!/usr/bin/python
from __future__ import unicode_literals
from logging import getLogger
from time import sleep
from django.conf import settings
from api.exceptions import DiskNotAvailableException
import httplib2
from .cloud import Cloud

try:
    from apiclient import discovery
    from oauth2client import client
except:
    pass


logger = getLogger(__name__)


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
                'imageName': '',
                'ip':'' }
        return self._gce_params

    def __getstate__(self):
        if hasattr(self, '_gce_params'):
            odict = self.__dict__.copy()
            del odict['_gce_params']
            return odict
        else:
            return self.__dict__

    def getInstanceName(self, node):
        return node.instance_id

    def getDiskName(self):
        return self.gce['name'] + '-disk'

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

    def _getInstanceObjects(self, matchNames=None):
        # Fetch the instance
        request = self.gce['service'].instances().list(project=self.gce['project'], zone=self.gce['zone'])
        response = request.execute(http=self.gce['auth_http'])
        try:
            items = response['items']
        except:
            items = []
        return self.filterNames(items, matchNames)

    def _createInstance(self, userData=None):
        # Construct the request body
        disk_body = [
            {'source': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/disks/%(diskName)s" % self.gce,
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
        metadata_items = []
        if userData:
            metadata_items = [{"key": "user-data", "value": userData}]
        body = {
            'name': self.gce['name'],
            'kernel': 'https://www.googleapis.com/compute/v1beta16/projects/%(kernel)s' % self.gce,
            'machineType': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/machineTypes/%(machineType)s" % self.gce,
            'networkInterfaces': netIfc_body,
            'disks': disk_body,
            'description': '%(name)s instance' % self.gce,
            'metadata': {'items': metadata_items}
        }
        # Create the instance
        request = self.gce['service'].instances().insert(project=self.gce['project'], body=body, zone=self.gce['zone'])
        response = request.execute(http=self.gce['auth_http'])
        return response

    def _deleteInstance(self, waitFunction=None):
        # Delete the instance (but not the persistent disk).
        request = self.gce['service'].instances().delete(project=self.gce['project'], zone=self.gce['zone'], instance=self.gce['name'])
        response = request.execute(http=self.gce['auth_http'])

        if waitFunction is not None:
            #
            # Wait for Shutdown to occur.
            #
            for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
                if not waitFunction():
                    break
                sleep(GoogleComputeEngine.RETRY_DELAY)

        return response

    def _getDiskObjects(self, matchNames=None):
        # Fetch the instance
        request = self.gce['service'].disks().list(project=self.gce['project'], zone=self.gce['zone'])
        response = request.execute(http=self.gce['auth_http'])
        try:
            items = response['items']
        except:
            items = []
        return self.filterNames(items, matchNames)

    def _createDisk(self, diskSize, wait=False):
        #
        # Create a persistent Disk for the Instance to mount
        #
        body = {
            "name": self.gce["diskName"],
            "sizeGb": str(diskSize),
            "description": "GenieDB disk",
        }

        request = self.gce['service'].disks().insert(project=self.gce['project'], body=body, sourceImage=self.gce['sourceImage'], zone=self.gce['zone'])
        response = request.execute(http=self.gce['auth_http'])

        if wait:
            #
            # Ensure that the persistent disk is ready to use
            #
            sleep(2)
            diskIsReady = False
            for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
                disks = self._getDiskObjects(self.gce["diskName"])
                if disks and disks[0]['status'] == 'READY':
                    diskIsReady = True
                    break
                sleep(GoogleComputeEngine.RETRY_DELAY)
            if not diskIsReady:
                raise DiskNotAvailableException

        return response

    def _deleteDisk(self):
        # Delete the persistent disk
        request = self.gce['service'].disks().delete(project=self.gce['project'], zone=self.gce['zone'], disk=self.gce['diskName'])
        response = request.execute(http=self.gce['auth_http'])
        return response

    def launch(self, node):
        project = self.gce['project']
        zone = self.region.code
        self.gce['zone'] = zone
        self.gce['name'] = make_gce_valid_name('dbaas-cluster-{c}-node-{n}'.format(c=node.cluster.pk, n=node.nid))
        diskName = self.getDiskName()
        self.gce['diskName'] = diskName
        self.gce['nid'] = node.nid
        self.gce['machineType'] = node.flavor.code
        self.gce['imageName'] = node.region.image
        sourceImage = 'https://www.googleapis.com/compute/v1beta16/projects/%(project)s/global/images/%(imageName)s' % self.gce
        self.gce['sourceImage'] = sourceImage

        #
        # Create a persistent Disk for the Instance to mount
        #
        self._createDisk(diskSize=node.storage, wait=True)

        #
        # Create the Instance
        #
        self._createInstance(userData=self.cloud_init(node))
        logger.info("Creating the GCE Instance %(name)s" % (self.gce))
        node.instance_id = self.gce['name']
        node.security_group = self.gce['zone']
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        items = self._getInstanceObjects(self.gce['name'])
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
        items = self._getInstanceObjects(self.gce['name'])
        return items != []

    def reinstantiating(self, node):
        return self.pending(node)

    def getIP(self, node):
        ip = ''
        items = self._getInstanceObjects(node.instance_id)
        if items:
            try:
                ip = items[0]['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            except:
                pass
        return ip

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
            response = request.execute(http=self.gce['auth_http'])

    def terminate(self, node):
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        diskName = self.getDiskName()
        self.gce['diskName'] = diskName
        if node.instance_id != "":
            self.gce['name'] = node.instance_id
            if node.status != node.SHUTTING_DOWN:
                node.status = node.SHUTTING_DOWN
                node.save()
            #
            # Delete the instance
            #
            logger.debug("Terminating GCE Instance %(name)s" % self.gce)
            self._deleteInstance(waitFunction=node.shutting_down)

            #
            # We also need to delete the persistent disk.
            #
            self._deleteDisk()
            node.instance_id = ""

    def reinstantiate(self, node):
        # Note: this command reboots the server as a new instance
        self.gce['name'] = node.instance_id
        self.gce['zone'] = node.security_group
        diskName = self.getDiskName()
        self.gce['diskName'] = diskName
        self.gce['nid'] = node.nid
        self.gce['machineType'] = node.flavor.code
        self.gce['imageName'] = node.region.image
        sourceImage = 'https://www.googleapis.com/compute/v1beta16/projects/%(project)s/global/images/%(imageName)s' % self.gce
        self.gce['sourceImage'] = sourceImage

        #
        # Delete the instance
        #
        self._deleteInstance(waitFunction=node.shutting_down)

        #
        # Reinstantiate the instance with its new configuration
        #
        self._createInstance(userData=self.cloud_init(node))
        logger.info("Reinstantiating the GCE Instance %(name)s" % (self.gce))
        #node.instance_id = self.gce['name']
        #node.security_group = self.gce['zone']
        node.status = node.PROVISIONING
        node.save()

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



