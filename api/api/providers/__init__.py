#!/usr/bin/python

from __future__ import unicode_literals
from aws import EC2 as az
from cloud import Cloud as test
from pb import ProfitBrick as pb
from gce import GoogleComputeEngine as gce

def rs(region):
    import openstack
    if region.code == 'lon':
        return openstack.RackspaceLondon(region)
    else:
        return openstack.Rackspace(region)
