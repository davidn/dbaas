from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
import httplib2
from api.cloud import Cloud, remove_trail_slash, retry

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
    GDB_IMAGE_NAME      = settings.GCE_IMAGE_NAME

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
                'imageName':GoogleComputeEngine.GDB_IMAGE_NAME,
                'ip':'' }
        return self._gce_params

    def __getstate__(self):
        if hasattr(self, '_gce_params'):
            odict = self.__dict__.copy()
            del odict['_gce_params']
            return odict
        else:
            return self.__dict__

    def getDiskName(self, name):
        return name + '-disk'

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
        project = self.gce['project']
        zone = self.region.name
        self.gce['zone'] = zone
        self.gce['name'] = make_gce_valid_name('dbaas-cluster-{c}-node-{n}'.format(c=node.cluster.pk, n=node.nid))
        diskName = self.gce['name'] + '-disk'
        self.gce['diskName'] = diskName
        self.gce['nid'] = node.nid
        self.gce['machineType'] = node.flavor.name
        sourceImage = 'https://www.googleapis.com/compute/v1beta16/projects/%(project)s/global/images/%(imageName)s' % self.gce
        self.gce['sourceImage'] = sourceImage
        logger.debug("%(name)s: Assigned NID %(nid)s" % self.gce)

        #
        # Create a persistent Disk for the Instance to mount
        #
        body = {
          "name": diskName,
          "sizeGb": str(node.storage),
          "description": "GenieDB disk",
        }

        request = self.gce['service'].disks().insert(project=project, body=body, sourceImage=sourceImage, zone=zone)
        response = request.execute(self.gce['auth_http'])

        sleep(2)
        for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
            disks = self.getDiskObjects(diskName)
            if disks and disks[0]['status'] == 'READY':
                break
            sleep(GoogleComputeEngine.RETRY_DELAY)

        #
        # Create the Instance
        #
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
        user_data = \
            '#include\nhttps://' + Site.objects.get_current().domain + remove_trail_slash(node.get_absolute_url()) + '/cloud_config/\n'
        metadata_items = [{"key": "user-data", "value": user_data}]
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
        diskName = self.gce['name'] + '-disk'
        self.gce['diskName'] = diskName
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
            request = self.gce['service'].disks().delete(project=self.gce['project'], zone=self.gce['zone'], disk=self.gce['diskName'])
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



