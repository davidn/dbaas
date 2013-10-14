from logging import getLogger
from time import sleep
from django.conf import settings
from django.contrib.sites.models import Site
import httplib2
from .utils import retry

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

    def pausing(self, node):
        pass

    def resuming(self, node):
        pass

    def update(self, node, tags={}):
        pass

    def terminate(self, node):
        pass

    def pause(self, node):
        pass

    def resume(self, node):
        pass



