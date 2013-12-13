#!/usr/bin/python
from __future__ import unicode_literals
from logging import getLogger
from django.conf import settings
from .cloud import Cloud
from api.utils import retry
import pb.client
import suds

logger = getLogger(__name__)


class ProfitBrick(Cloud):
    USER = settings.PROFITBRICK_USER
    PASS = settings.PROFITBRICK_PASS

    @property
    def pbp(self):
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
        logger.debug("Creating the DataCenter - %s, %s", self.region.name, self.region.code)
        node.security_group = self.pbp.createDataCenter(str(node), self.region.code).dataCenterId
        retry(lambda: provisioning_state_available(self.pbp.getDataCenter(node.security_group)))

        # Create the Server
        logger.debug("Creating the Server - name=%s, cores=%d, ram=%d, datacenter=%s", node, node.flavor.cpus,
                     node.flavor.ram, node.security_group)
        node.instance_id = self.pbp.createServer({
            'serverName': str(node),
            'cores': node.flavor.cpus,
            'ram': node.flavor.ram,
            'dataCenterId': node.security_group,
            #'availabilityZone': self.region.code,
            'internetAccess': True}).serverId
        #retry(lambda: provisioning_state_available(self.pbp.getServer(srvId)), initialDelay=250)

        # Create the Storage
        logger.debug("Creating the Storage - size=%d", node.storage)
        # Find the image object
        image_id = None
        images = self.pbp.getAllImages()
        for image in images:
            if image['imageName'] == self.region.image and image['region'] == self.region.code:
                image_id = image['imageId']
                break
        logger.debug("mounting image=%s, Id=%s" % (self.region.image, str(image_id)))
        storage_id = self.pbp.createStorage({
            'size': node.storage,
            'dataCenterId': node.security_group,
            'mountImageId': image_id,
            'storageName': str(node)}).storageId
        #retry(lambda: provisioning_state_available(self.pbp.getStorage(stgId)))

        # Connect the Server to the Storage
        self.pbp.connectStorageToServer({"storageId": storage_id, "serverId": node.instance_id})
        logger.debug("Connected the Storage to the Server - stgId=%s, svrId=%s" % (storage_id, node.instance_id))

    def pending(self, node):
        svr = self.pbp.getServer(node.instance_id)
        if svr and svr.provisioningState == 'AVAILABLE':
            return False
        return True

    def shutting_down(self, node):
        try:
            self.pbp.getDataCenter(node.security_group)
            return True
        except:
            return False

    def reinstantiating(self, node):
        svr = self.pbp.getServer(node.instance_id)
        if svr and svr.provisioningState == 'AVAILABLE' and svr.cores == node.flavor.cpus and \
                svr.ram == node.flavor.ram:
            return False
        return True

    def reinstantiate(self, node):
        tags = {"serverId": node.instance_id,
                "cores": node.flavor.cpus,
                "ram": node.flavor.ram}
        self.pbp.updateServer(tags)
        logger.info("Reinstantiating the PB Instance %s", node.instance_id)

    def get_ip(self, node):
        s = self.pbp.getServer(node.instance_id)
        return s.ips[0]

    def update(self, node, tags=None):
        supported_properties = ['serverName', 'cores', 'ram', 'bootFromImageId', 'availabilityZone',
                                'bootFromStorageId', 'osType']
        if tags is None:
            tags = {}
        for k in tags.keys():
            if k not in supported_properties:
                del tags[k]
        if tags:
            tags['serverId'] = node.instance_id
            logger.debug("PB.update: tags=%s" % (str(tags)))
            self.pbp.updateServer(tags)

    def terminate(self, node):
        if node.instance_id != "":
            try:
                logger.debug("%s: terminating server %s", node, node.instance_id)
                self.pbp.deleteServer(node.instance_id)
            except suds.WebFault, e:
                if e.fault.detail.ProfitbricksServiceFault.httpCode != 404:
                    raise
            node.instance_id = ""
        if node.security_group != "":
            try:
                logger.debug("%s: terminating security group %s", node, node.security_group)
                self.pbp.deleteDataCenter(node.security_group)
            except suds.WebFault, e:
                if e.fault.detail.ProfitbricksServiceFault.httpCode != 404:
                    raise
            node.security_group = ""


def provisioning_state_available(obj):
    if obj.provisioningState == 'AVAILABLE':
        return object
