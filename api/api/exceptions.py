#!/usr/bin/python
from __future__ import unicode_literals


class BackendNotReady(Exception):
    pass


class DiskNotAvailableException(Exception):
    pass


class LaunchException(Exception):
    pass
