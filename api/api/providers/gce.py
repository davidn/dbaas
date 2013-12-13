#!/usr/bin/python
from __future__ import unicode_literals
from logging import getLogger
from time import sleep
from django.conf import settings
from api.exceptions import DiskNotAvailableException
import httplib2
from .cloud import Cloud
from apiclient import discovery, errors
from oauth2client import client


logger = getLogger(__name__)


class GoogleComputeEngine(Cloud):
    SERVICE_PROJECT_ID = settings.GCE_PROJECT_ID
    SERVICE_ACCT_EMAIL = settings.GCE_SERVICE_ACCOUNT_EMAIL
    SERVICE_PRIVATE_KEY = settings.GCE_PRIVATE_KEY

    MAX_DELAY_RETRIES = 40        # Max delay of 200 seconds
    RETRY_DELAY = 5

    @property
    def http(self):
        if not hasattr(self, "_http"):
            credentials = client.SignedJwtAssertionCredentials(
                service_account_name=GoogleComputeEngine.SERVICE_ACCT_EMAIL,
                private_key=GoogleComputeEngine.SERVICE_PRIVATE_KEY,
                scope=['https://www.googleapis.com/auth/compute',
                       'https://www.googleapis.com/auth/devstorage.full_control',
                       'https://www.googleapis.com/auth/devstorage.read_write'])
            self._http = credentials.authorize(httplib2.Http())
        return self._http


    @property
    def gce(self):
        if not hasattr(self, "_gce"):
            self._gce = discovery.build('compute', 'v1beta16', http=self.http)
        return self._gce

    def __getstate__(self):
        if hasattr(self, '_gce'):
            odict = self.__dict__.copy()
            del odict['_gce']
            return odict
        else:
            return self.__dict__

    @staticmethod
    def node_name(node):
        return make_gce_valid_name('dbaas-cluster-{c}-node-{n}'.format(c=node.cluster.pk, n=node.nid))

    def get_disk_name(self, node):
        return node.instance_id + '-disk'

    @staticmethod
    def filter_names(items, match_names=None):
        if match_names is not None:
            all_items = items
            items = []
            if isinstance(match_names, basestring):
                match_names = [match_names]
            for item in all_items:
                if item['name'] in match_names:
                    items.append(item)
        return items

    def _get_instance_objects(self, match_names=None):
        # Fetch the instance
        request = self.gce.instances().list(project=self.SERVICE_PROJECT_ID, zone=self.region.code)
        response = request.execute(http=self.http)
        return self.filter_names(response.get('items', []), match_names)

    def _create_instance(self, node, user_data=None):
        # Construct the request body
        disk_body = [{
            'source': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/disks/%(disk_name)s" % {
                'project': self.SERVICE_PROJECT_ID,
                'zone': self.region.code,
                'disk_name': self.get_disk_name(node)
            },
            'boot': True,
            'type': 'PERSISTENT',
            'mode': 'READ_WRITE',
            'deviceName': "bootdisk",
        }]
        net_body = [{
            'accessConfigs': [{'type': 'ONE_TO_ONE_NAT',
                               'name': 'External NAT'}],
            'network': 'https://www.googleapis.com/compute/v1beta16/projects/%s/global/networks/default' % self.SERVICE_PROJECT_ID,
        }]
        metadata_items = []
        if user_data:
            metadata_items = [{"key": "user-data", "value": user_data}]
        body = {
            'name': node.instance_id,
            'kernel': 'https://www.googleapis.com/compute/v1beta16/projects/google/global/kernels/gce-v20130813',
            'machineType': "https://www.googleapis.com/compute/v1beta16/projects/%(project)s/zones/%(zone)s/machineTypes/%(machine_type)s" % {
                'project': self.SERVICE_PROJECT_ID,
                'zone': self.region.code,
                'machine_type': self.node.flavor.code
            },
            'networkInterfaces': net_body,
            'disks': disk_body,
            'metadata': {'items': metadata_items}
        }
        # Create the instance
        request = self.gce.instances().insert(project=self.SERVICE_PROJECT_ID, body=body, zone=self.region.code)
        response = request.execute(http=self.http)
        return response

    def _delete_instance(self, node, wait_function=None):
        # Delete the instance (but not the persistent disk).
        request = self.gce.instances().delete(project=self.SERVICE_PROJECT_ID, zone=self.region.code,
                                              instance=node.instance_id)
        response = request.execute(http=self.http)

        if wait_function is not None:
            #
            # Wait for Shutdown to occur.
            #
            for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
                if not wait_function():
                    break
                sleep(GoogleComputeEngine.RETRY_DELAY)

        return response

    def _get_disk_objects(self, match_names=None):
        # Fetch the instance
        request = self.gce.disks().list(project=self.SERVICE_PROJECT_ID, zone=self.region.code)
        response = request.execute(http=self.http)
        return self.filter_names(response.get('items', []), match_names)

    def _create_disk(self, node, wait=False):
        #
        # Create a persistent Disk for the Instance to mount
        #
        body = {
            "name": self.get_disk_name(node),
            "sizeGb": str(node.storage),
            "description": "GenieDB disk",
        }

        request = self.gce.disks().insert(
            project=self.SERVICE_PROJECT_ID,
            body=body,
            sourceImage='https://www.googleapis.com/compute/v1beta16/projects/%s/global/images/%s' % (
                self.SERVICE_PROJECT_ID, node.region.image),
            zone=self.region.code)
        response = request.execute(http=self.http)

        if wait:
            #
            # Ensure that the persistent disk is ready to use
            #
            sleep(2)
            disk_ready = False
            for i in xrange(GoogleComputeEngine.MAX_DELAY_RETRIES):
                disks = self._get_disk_objects(self.get_disk_name(node))
                if disks and disks[0]['status'] == 'READY':
                    disk_ready = True
                    break
                sleep(GoogleComputeEngine.RETRY_DELAY)
            if not disk_ready:
                raise DiskNotAvailableException

        return response

    def _delete_disk(self, node):
        # Delete the persistent disk
        request = self.gce.disks().delete(project=self.SERVICE_PROJECT_ID, zone=self.region.code,
                                          disk=self.get_disk_name(node))
        response = request.execute(http=self.http)
        return response

    def launch(self, node):
        node.instance_id = self.node_name(node)
        self._create_disk(wait=True)
        self._create_instance(user_data=self.cloud_init(node))
        logger.info("Creating GCE Instance")

    def pending(self, node):
        items = self._get_instance_objects(node.instance_id)
        if items and items[0]['status'] == 'RUNNING':
            return False
        return True

    def shutting_down(self, node):
        return self._get_instance_objects(node.instance_id) != []

    reinstantiating = pending

    def get_ip(self, node):
        try:
            return self._get_instance_objects(node.instance_id)[0]['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        except (KeyError, IndexError):
            return ""

    def update(self, node, tags=None):
        supported_properties = []   # Put in the list of supported metadata properties when they are known.
        body = {"items": []}
        if tags is None:
            tags = {}
        for k in tags.keys():
            if k not in supported_properties:
                del tags[k]
        if tags:
            body['items'].append({"name": node.instance_id})  # Is this the right property name?
            for k, v in tags.items():
                body['items'].append({k: v})
            request = self.gce.instances().setMetadata(project=self.SERVICE_PROJECT_ID, zone=self.region.code,
                                                       instance=node.instance_id, body=body)
            request.execute(http=self.http)

    def terminate(self, node):
        if node.instance_id != "":
            logger.debug("Terminating GCE Instance")
            try:
                self._delete_instance(wait_function=node.shutting_down)
            except errors.HttpError, e:
                if e.resp.status != 404:
                    raise
            try:
                self._delete_disk()
            except errors.HttpError, e:
                if e.resp.status != 404:
                    raise
            node.instance_id = ""

    def reinstantiate(self, node):
        # Note: this command reboots the server as a new instance
        self._delete_instance(wait_function=node.shutting_down)
        self._create_instance(user_data=self.cloud_init(node))
        logger.info("Reinstantiating the GCE Instance")

def make_gce_valid_name(name):
    MAX_VALID_NAME_LEN = 63    # GCE Instance Names must be <= this length
    FIRST_ALPHA = "g"   # GCE Name must start with an alpha char
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
