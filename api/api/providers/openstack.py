from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
from api.cloud import Cloud, remove_trail_slash, retry

import novaclient.v1_1

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



