
from aws import EC2 as az
from cloud import Cloud as test
from profitbricks import ProfitBrick as pb
from gce import GoogleComputeEngine as gce

def rs(region):
    import openstack
    if region.code == 'lon':
        return openstack.RackspaceLondon(region)
    else:
        return openstack.Rackspace(region)
