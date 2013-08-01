#!/usr/bin/python

from time import sleep
import re
from Crypto import Random
from Crypto.PublicKey import RSA
from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from logging import getLogger
import boto.ec2
from .route53 import RecordWithHealthCheck, HealthCheck, record, exception
from boto import connect_route53
from .uuid_field import UUIDField
from api.route53 import RecordWithTargetHealthCheck
import novaclient.v1_1

logger = getLogger(__name__)

class EC2Regions(object):
    def __init__(self):
        self._regions = {}
    
    def __getitem__(self,key):
        if not self._regions.has_key(key):
            self._regions[key] = boto.ec2.get_region(key).connect(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        return self._regions[key]

ec2regions = EC2Regions()


class CloudCompute(object):
    def __init__(self, region):
        self.region = region

    def launch(self, node):
        pass

    def pending(self, node):
        pass

    def shutting_down(self, node):
        pass

    def update(self, node, tags={}):
        pass

    def terminate(self, node):
        pass

    def pause(self, node):
        pass

    def resume(self, node):
        pass

class EC2(CloudCompute):
    def __init__(self, region):
        super(EC2, self).__init__(region)
        self.ec2 = ec2regions[self.region[3:]]

    def launch(self, node):
        # Elastic Block Storage
        dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType(iops=node.iops, volume_type=node.volume_type)
        dev_sda1.size = node.storage
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1
        logger.debug("%s: Assigned NID %s", node, node.nid)
        sg = self.ec2.create_security_group(str(node),'Security group for '+str(node))
        node.security_group = sg.id
        self.ec2.authorize_security_group(
            group_id=sg.id,
            ip_protocol='tcp',
            cidr_ip='0.0.0.0/0',
            from_port=node.cluster.port,
            to_port=node.cluster.port)
        logger.debug("%s: Created Security Group %s (named %s) with port %s open", node, sg.id, sg.name, node.port)
        node.save()
        # EC2 Instance
        try:
            sgs = settings.REGIONS[self.region]['SECURITY_GROUPS'] + [sg.name]
        except KeyError:
            sgs = [sg.name]
        try:
            res = self.ec2.run_instances(
                settings.REGIONS[self.region]["IMAGE"],
                key_name=settings.REGIONS[self.region]['KEY_NAME'],
                instance_type=node.size,
                block_device_map=bdm,
                security_groups=sgs,
                user_data ='#include\nhttps://'+Site.objects.get_current().domain+node.get_absolute_url()+'cloud_config/',
            )
        except:
            try:
                self.ec2.delete_security_group(group_id=node.security_group)
            except:
                pass
            raise
        node.instance_id = res.instances[0].id
        logger.debug("%s: Reservation %s launched. Instance id %s", node, res.id, node.instance_id)
        node.status = node.PROVISIONING
        node.save()

    def pending(self, node):
        return self.ec2.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].update() == 'pending'

    def shutting_down(self, node):
        return self.ec2.get_all_instances(instance_ids=[self.instance_id])[0].instances[0].update() == 'shutting-down'

    def update(self, node, tags={}):
        instance = self.ec2.get_all_instances(instance_ids=[self.instance_id])[0].instances[0]
        node.ip = instance.ip_address
        node.save()
        for k,v in tags.items():
            instance.add_tag(k, v)

    def terminate(self, node):
        self.ec2.terminate_instances([node.instance_id])
        if node.security_group != "":
            node.status = self.SHUTTING_DOWN
            node.save()
            while node.shutting_down():
                sleep(15)
            logger.debug("%s: terminating security group %s", node, node.security_group)
            self.ec2.delete_security_group(group_id=node.security_group)

    def pause(self, node):
        ec2regions[self.region.region].stop_instances([self.instance_id])

    def resume(self, node):
        ec2regions[self.region.region].start_instances([self.instance_id])

class Openstack(CloudCompute):
    def __init__(self, region):
        super(Openstack, self).__init__(region)
        self.nova = novaclient.v1_1.client.Client(self.USER,
            self.PASS,
            self.TENANT,
            self.AUTH_URL,
            service_type="compute",
            region_name=region[3:])

    def launch(self, node):
        server = self.nova.servers.create(
            name= node.dns_name,
            image=settings.REGIONS[self.region]['IMAGE'],
            flavor=node.size,
            key_name=settings.REGIONS[self.region]['KEY_NAME'],
            availability_zone=self.region[3:],
        )
        node.instance_id = server.id
        node.status=Node.PROVISIONING

    def pending(self, node):
        return self.nova.servers.get(node.instance_id).status == u'BUILD'

    def shutting_down(self, node):
        return self.nova.servers.get(node.instance_id).status == u'STOPPING'

    def update(self, node, tags={}):
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

class Cluster(models.Model):
    user = models.ForeignKey(User)
    uuid = UUIDField(primary_key=True)
    port = models.PositiveIntegerField("MySQL Port", default=settings.DEFAULT_PORT)
    dbname = models.CharField("Database Name", max_length=255)
    dbusername = models.CharField("Database Username", max_length=255)
    dbpassword = models.CharField("Database Password", max_length=255)

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.dns_name

    @models.permalink
    def get_absolute_url(self):
        return ('cluster-detail', [self.pk])

    def next_nid(self):
        return max([node.nid for node in self.nodes.all()]+[0])+1

    @property
    def dns_name(self):
        return settings.CLUSTER_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.'+str(node.nid), "5502"]) for node in self.nodes.all())

    def get_region_set(self, region):
        obj, _ = self.regions.get_or_create(cluster=self.pk, region=region)
        return obj

def gen_private_key():
    return RSA.generate(2048, Random.new().read).exportKey()

class RegionNodeSet(models.Model):
    cluster = models.ForeignKey(Cluster, related_name='regions')
    region = models.CharField("EC2 Region", max_length=20)
    launched = models.BooleanField("Launched")

    def __unicode__(self):
        return self.dns_name

    @property
    def dns_name(self):
        return settings.REGION_DNS_TEMPLATE.format(cluster=self.cluster.pk, region=self.region)

    def do_launch(self):
        logger.debug("%s: setting up dns for region %s, cluster %s", self, self.region, self.cluster.pk)
        r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
        rrs.add_change_record('CREATE', self.record)
        rrs.commit()
        self.launched = True
        self.save()

    @property
    def identifier(self):
        return "%s-%s" % (self.cluster.pk, self.region)

    @property
    def record(self):
        return RecordWithTargetHealthCheck(name=self.cluster.dns_name,
            type='A', ttl=60, alias_hosted_zone_id=settings.ROUTE53_ZONE, alias_dns_name=self.dns_name,
            identifier=self.identifier, region=self.region)

    @property
    def connection(self):
        if self.region[0:2] == "az":
            return EC2()
        elif self.region[0:2] == "rs":
            return Rackspace()

        raise KeyError("Unknown Region")
    def on_terminate(self):
        logger.debug("%s: terminating dns for region %s, cluster %s", self, self.region, self.cluster.pk)
        r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
        rrs.add_change_record('DELETE', self.record)
        try:
            rrs.commit()
        except exception.DNSServerError, e:
            if re.search('but it was not found', e.body) is None:
                raise
            else:
                logger.warning("%s: terminating dns for region %s, cluster %s skipped as record not found")

class Node(models.Model):
    INITIAL=0
    PROVISIONING=3
    INSTALLING_CF=4
    RUNNING=6
    SHUTTING_DOWN=7
    OVER=8
    PAUSED=9
    ERROR=1000
    STATUSES = (
        (INITIAL, 'not yet started'),
        (PROVISIONING, 'Provisioning EC2 instances'),
        (INSTALLING_CF, 'Installing GenieDB CloudFabric'),
        (RUNNING, 'running'),
        (PAUSED, 'paused'),
        (SHUTTING_DOWN, 'shutting down'),
        (OVER, 'over'),
        (ERROR, 'An error occured')
    )
    instance_id = models.CharField("EC2 Instance ID", max_length=200, default="", blank=True)
    security_group = models.CharField("EC2 Security Group ID", max_length=200, default="", blank=True)
    health_check = models.CharField("R53 Health Check ID", max_length=200, default="", blank=True)
    nid = models.IntegerField("Node ID", default=None, blank=True, null=True)
    region = models.ForeignKey(RegionNodeSet, related_name='nodes')
    size = models.CharField("Size", max_length=20)
    storage = models.IntegerField("Allocated Storage")
    ip = models.IPAddressField("EC2 Instance IP Address", default="", blank=True)
    iops = models.IntegerField("Provisioned IOPS", default=None, blank=True, null=True)
    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    tinc_private_key = models.TextField("Tinc Private Key", default=gen_private_key)
    cluster = models.ForeignKey(Cluster, related_name='nodes')

    def __repr__(self):
        optional = ""
        if self.iops != "":
            optional += ", iops={iops}".format(iops=repr(self.iops))
        if self.instance_id != "":
            optional += ", instance_id={instance_id}".format(instance_id=repr(self.instance_id))
        if self.status != "":
            optional += ", status={status}".format(status=repr(self.status))
        if self.ip != "":
            optional += ", ip={ip}".format(ip=repr(self.ip))
        return "Node(pk={pk}, cluster={cluster}, size={size}, storage={storage}, region={region}{optional})".format(
            pk=repr(self.pk),
            cluster=repr(self.cluster),
            size=repr(self.size),
            storage=repr(self.storage),
            region=repr(self.region.region),
            optional=optional
        )

    def __unicode__(self):
        return self.dns_name

    def pending(self):
        return self.region.connection.pending(self)

    def shutting_down(self):
        return self.region.connection.shutting_down(self)

    def update(self, tags={}):
        return self.region.connection.update(self, tags)

    @models.permalink
    def get_absolute_url(self):
        return ('node-detail', [self.cluster.pk, self.pk])

    @property
    def dns_name(self):
        return settings.NODE_DNS_TEMPLATE.format(cluster=self.cluster.pk, node=self.nid)

    @property
    def volume_type(self):
        if self.iops is None:
            return None
        else:
            return 'io1'

    @property
    def public_key(self):
        return RSA.importKey(self.tinc_private_key).publickey().exportKey()

    @property
    def buffer_pool_size(self):
        return int(max(settings.INSTANCE_TYPES[self.size]["ram"]*0.8, settings.INSTANCE_TYPES[self.size]["ram"]-2)*2**30)

    @property
    def cloud_config(self):
        connect_to_list = "\n    ".join("ConnectTo = node_"+str(node.nid) for node in self.cluster.nodes.all())
        rsa_priv = self.tinc_private_key.replace("\n", "\n    ")
        host_files = "\n".join("""- content: |
    Address={address}
    Subnet=192.168.33.{nid}/32
    {rsa_pub}
  path: /etc/tinc/cf/hosts/node_{nid}
  owner: root:root
  permissions: '0644'""".format(nid=node.nid,address=node.dns_name,rsa_pub=node.public_key.replace("\n","\n    ")) for node in self.cluster.nodes.all())
        return  """#cloud-config
write_files:
- content: |
    [mysqld]
    auto_increment_offset={nid}
    auto_increment_increment=255
    geniedb_my_node_id={nid}
    geniedb_subscriptions={subscriptions}
    geniedb_buffer_pool_size={buffer_pool_size}
    default_storage_engine=GenieDB
    port={port}
  path: /etc/mysql/conf.d/geniedb.cnf
  owner: root:root
  permissions: '0644'
- content: |
   CREATE DATABASE {dbname};
   CREATE USER '{dbusername}'@'%' IDENTIFIED BY '{dbpassword}';
   GRANT ALL ON {dbname}.* to '{dbusername}'@'%';
  path: /etc/mysqld-grants
  owner: root:root
  permissions: '0644'
- content: |
    Name = node_{nid}
    Device = /dev/net/tun
    {connect_to_list}
  path: /etc/tinc/cf/tinc.conf
  owner: root:root
  permissions: '0644'
- content: |
    #!/bin/sh
    ip addr flush cf
    ip addr add 192.168.33.{nid}/24 dev cf
    ip link set cf up
  path: /etc/tinc/cf/tinc-up
  owner: root:root
  permissions: '0755'
- content: |
  path: /etc/tinc/cf/rsa_key.priv
  owner: root:root
  permissions: '0600'
  content: |
    {rsa_priv}
{host_files}
runcmd:
- [lokkit, -p, "{port}:tcp"]
""".format(nid=self.nid,
           port=self.cluster.port,
           subscriptions=self.cluster.subscriptions,
           dbname=self.cluster.dbname,
           dbusername=self.cluster.dbusername,
           dbpassword=self.cluster.dbpassword,
           connect_to_list=connect_to_list,
           rsa_priv=rsa_priv,
           host_files=host_files,
           buffer_pool_size=self.buffer_pool_size)

    def do_launch(self):
        """Do the initial, fast part of launching this node."""
        self.nid = self.cluster.next_nid()
        logger.debug("%s: Assigned NID %s", self, self.nid)
        logger.info("%s: provisioning node", self)
        try:
            self.region.connection.launch(self)
        except:
            self.status = self.ERROR
            self.save()
            raise
        self.status = self.PROVISIONING
        self.save()

    def do_install(self):
        """Do slower parts of launching this node."""
        while self.pending():
            sleep(15)
        self.update({
            'Name':'dbaas-cluster-{c}-node-{n}'.format(c=self.cluster.pk, n=self.nid),
            'username':self.cluster.user.username,
            'cluster':str(self.cluster.pk),
            'node':str(self.pk),
            'url':'https://'+Site.objects.get_current().domain+self.get_absolute_url(),
        })
        r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        health_check = HealthCheck(connection=r53, caller_reference=self.instance_id,
            ip_address=self.ip, port=self.cluster.port, health_check_type='TCP')
        self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
        rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
        rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.region.dns_name,
            type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, weight=1))
        rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
            resource_records=[self.ip]))
        rrs.commit()
        self.status = self.RUNNING
        self.save()
        #... wait until node has fetched config and installed and tests run...
        # self.status = self.RUNNING
        # self.save()

    def pause(self):
        assert(self.status == Node.RUNNING)
        self.connection.pause(self)
        self.status = Node.PAUSED
        self.save()

    def resume(self):
        assert(self.status == Node.PAUSED)
        self.connection.resume(self)
        self.status = Node.RUNNING
        self.save()

    def on_terminate(self):
        if self.status in (self.PROVISIONING, self.INSTALLING_CF, self.RUNNING, self.PAUSED, self.ERROR):
            logger.debug("%s: terminating instance %s", self, self.instance_id)
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.region.dns_name,
                type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, weight=1))
            rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                resource_records=[self.ip]))
            rrs.commit()
            r53.delete_health_check(self.health_check)
            self.region.connection.terminate(self)

@receiver(models.signals.pre_delete, sender=Node)
def node_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Node:
        return
    instance.on_terminate()

@receiver(models.signals.pre_delete, sender=RegionNodeSet)
def region_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != RegionNodeSet:
        return
    instance.on_terminate()
