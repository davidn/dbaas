from logging import getLogger
from textwrap import dedent
from django.conf import settings

logger = getLogger(__name__)

class Cloud(object):
    def __init__(self, region):
        self.region = region

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

    def pause(self, node):
        pass

    def resume(self, node):
        pass

    def cloud_init(self, node):
        return dedent("""\
            #!/bin/sh
            sed -i 's/#master: salt/master: {salt_master}/' /etc/salt/minion
            sed -i 's/#id:/id: {dns_name}/' /etc/salt/minion
            """.format(dns_name=node.dns_name, salt_master=settings.SALT_MASTER))
