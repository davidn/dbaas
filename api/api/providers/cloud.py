from logging import getLogger

logger = getLogger(__name__)

class Cloud(object):
    def __init__(self, region):
        self.region = region

    def getInstanceName(self, node):
        return node.dns_name

    def launch(self, node):
        pass

    def pending(self, node):
        return False

    def shutting_down(self, node):
        return False

    def pausing(self, node):
        return False

    def resuming(self, node):
        return False

    def update(self, node, tags={}):
        self.ip = "192.0.2.%d" % node.nid

    def terminate(self, node):
        pass

    def reinstantiate(self, node):
        # Note: this command reboots the server as a new instance
        pass

    def pause(self, node):
        pass

    def resume(self, node):
        pass
