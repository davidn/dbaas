from logging import getLogger
from django.conf import settings
from .cloud import Cloud

import novaclient.v1_1
import novaclient.exceptions

logger = getLogger(__name__)


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
                '/var/lib/cloud/seed/nocloud-net/user-data': self.cloud_init(node),
                '/var/lib/cloud/seed/nocloud-net/meta-data': 'instance-id: iid-local01',
            },
        )
        node.instance_id = server.id

    def pending(self, node):
        return self.nova.servers.get(node.instance_id).status == u'BUILD'

    def shutting_down(self, node):
        return self.nova.servers.get(node.instance_id).status == u'STOPPING'

    def reinstantiating(self, node):
        return self.nova.servers.get(node.instance_id).status == u'RESIZE'

    def get_ip(self, node):
        return self.nova.servers.get(node.instance_id).accessIPv4

    def update(self, node, tags=None):
        if tags is None:
            tags = {}
        tags['id'] = node.instance_id

    def terminate(self, node):
        try:
            self.nova.servers.delete(node.instance_id)
        except novaclient.exceptions.NotFound:
            pass

    def reinstantiate(self, node):
        self.nova.servers.resize(node.instance_id, flavor=node.flavor.code)
        logger.info("Reinstantiating the Openstack Instance %s" % (node.dns_name))

    def reinstantiation_complete(self, node):
        # Free up the original image before the resize snapshot.
        self.nova.servers.confirm_resize(node.instance_id)

class Rackspace(Openstack):
    USER = settings.RACKSPACE_USER
    PASS = settings.RACKSPACE_PASS
    TENANT = settings.RACKSPACE_TENANT
    AUTH_URL = settings.RACKSPACE_AUTH_URL

class RackspaceLondon(Rackspace):
    USER = settings.RACKSPACELONDON_USER
    PASS = settings.RACKSPACELONDON_PASS
    TENANT = settings.RACKSPACELONDON_TENANT
    AUTH_URL = settings.RACKSPACELONDON_AUTH_URL



