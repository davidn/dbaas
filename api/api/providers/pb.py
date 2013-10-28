from logging import getLogger
from time import sleep
from django.conf import settings
from .cloud import Cloud
from api.utils import retry

try:
    import pb.client
except:
    pass


logger = getLogger(__name__)


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
        retry(lambda: provisioningStateAvailable(self.pb.getDataCenter(dcId)))

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
        #retry(lambda: provisioningStateAvailable(self.pb.getServer(srvId)), initialDelay=250)

        # Create the Storage
        logger.debug("Creating the Storage - size=%d" % (node.storage))
        # Find the image object
        imageId = None
        images = self.pb.getAllImages()
        for image in images:
            if image['imageName'] == self.region.image and image['region'] == self.region.code:
                imageId = image['imageId']
                break
        logger.debug("mounting image=%s, Id=%s" % (self.region.image, str(imageId)))
        createStorageRequest = {
            'size': node.storage,
            'dataCenterId': dcId,
            'mountImageId': imageId,
            'storageName': str(node)}
        stgId = self.pb.createStorage(createStorageRequest).storageId
        #retry(lambda: provisioningStateAvailable(self.pb.getStorage(stgId)))

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

def provisioningStateAvailable(obj):
    if obj.provisioningState=='AVAILABLE':
        return object

