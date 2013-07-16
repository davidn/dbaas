#!/usr/bin/python

from time import sleep
from Crypto import Random
from Crypto.PublicKey import RSA
from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from logging import getLogger
import boto.ec2
import boto.connect_route53
from .route53 import RecordWithHealthCheck, HealthCheck, record
from .uuid_field import UUIDField

logger = getLogger(__name__)

class EC2Regions(object):
    def __init__(self):
        self._regions = {}
    
    def __getitem__(self,key):
        if not self._regions.has_key(key):
            self._regions[key] = boto.ec2.get_region(key).connect(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        return self._regions[key]

ec2regions = EC2Regions()

class Cluster(models.Model):
    user = models.ForeignKey(User)
    uuid = UUIDField(primary_key=True)

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.lbr_dns_name

    @models.permalink
    def get_absolute_url(self):
        return ('cluster-detail', [self.pk])

    def next_nid(self):
        return max([node.nid for node in self.nodes.all()]+[0])+1

    @property
    def lbr_dns_name(self):
        settings.LBR_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.'+str(node.nid), "5502"]) for node in self.nodes.all())

def gen_private_key():
    return RSA.generate(2048, Random.new().read).exportKey()

class Node(models.Model):
    INITIAL=0
    PROVISIONING=3
    INSTALLING_CF=4
    RUNNING=6
    SHUTTING_DOWN=7
    OVER=8
    ERROR=1000
    STATUSES = (
        (INITIAL, 'not yet started'),
        (PROVISIONING, 'Provisioning EC2 instances'),
        (INSTALLING_CF, 'Installing GenieDB CloudFabric'),
        (RUNNING, 'running'),
        (SHUTTING_DOWN, 'shutting down'),
        (OVER, 'over'),
        (ERROR, 'An error occured')
    )
    instance_id = models.CharField("EC2 Instance ID", max_length=200, default="", blank=True)
    security_group = models.CharField("EC2 Security Group ID", max_length=200, default="", blank=True)
    health_check = models.CharField("R53 Health Check ID", max_length=200, default="", blank=True)
    nid = models.IntegerField("Node ID", default=None, blank=True, null=True)
    region = models.CharField("EC2 Region", max_length=20)
    size = models.CharField("Size", max_length=20)
    storage = models.IntegerField("Allocated Storage")
    dns = models.CharField("EC2 Public DNS Address", max_length=200, default="", blank=True)
    ip = models.IPAddressField("EC2 Instance IP Address", default="", blank=True)
    port = models.PositiveIntegerField("MySQL Port", default=3306)
    iops = models.IntegerField("Provisioned IOPS", default=None, blank=True, null=True)
    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    tinc_private_key = models.TextField("Tinc Private Key", default=gen_private_key)
    mysql_setup = models.TextField("MySQL setup",blank=True)
    cluster = models.ForeignKey(Cluster, related_name='nodes')

    def __repr__(self):
        optional = ""
        if self.iops != "":
            optional += ", iops={iops}".format(iops=repr(self.iops))
        if self.instance_id != "":
            optional += ", instance_id={instance_id}".format(instance_id=repr(self.instance_id))
        if self.status != "":
            optional += ", status={status}".format(status=repr(self.status))
        if self.dns != "":
            optional += ", dns={dns}".format(dns=repr(self.dns))
        if self.ip != "":
            optional += ", ip={ip}".format(ip=repr(self.ip))
        if self.port != self.port.defult:
            optional += ", port={port}".format(port=repr(self.port))
        return "Node(pk={pk}, cluster={cluster}, size={size}, storage={storage}, region={region}{optional})".format(
            pk=repr(self.pk),
            cluster=repr(self.cluster),
            size=repr(self.size),
            storage=repr(self.storage),
            region=repr(self.region),
            optional=optional
        )

    def __unicode__(self):
        return self.dns_name

    def pending(self):
        return self.instance.update()=='pending'

    def shutting_down(self):
        return self.instance.update()=='shutting-down'

    def update(self, tags={}):
        self.dns = self.instance.public_dns_name
        self.ip = self.instance.ip_address
        self.save()
        for k,v in tags.items():
            self.instance.add_tag(k, v)

    @models.permalink
    def get_absolute_url(self):
        return ('node-detail', [self.cluster.pk, self.pk])

    @property
    def dns_name(self):
        settings.NODE_DNS_TEMPLATE.format(cluster=self.cluster.pk, nid=self.nid)

    @property
    def instance(self):
        if not hasattr(self, '_instance'):
            self._instance = ec2regions[self.region].get_all_instances(instance_ids=[self.instance_id])[0].instances[0]
        return self._instance

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
    def cloud_config(self):
        connect_to_list = "\n    ".join("ConnectTo = node_"+str(node.nid) for node in self.cluster.nodes.all())
        rsa_priv = self.tinc_private_key.replace("\n", "\n    ")
        host_files = "\n".join("""- content: |
    Address={address}
    Subnet=192.168.33.{nid}/32
    {rsa_pub}
  path: /etc/tinc/cf/hosts/node_{nid}
  owner: root:root
  permissions: '0644'""".format(nid=node.nid,address=node.dns,rsa_pub=node.public_key.replace("\n","\n    ")) for node in self.cluster.nodes.all())
        return  """#cloud-config
write_files:
- content: |
    [mysqld]
    auto_increment_offset={nid}
    auto_increment_increment=255
    geniedb_my_node_id={nid}
    geniedb_subscriptions={subscriptions}
    default_storage_engine=GenieDB
    port={port}
  path: /etc/mysql/conf.d/geniedb.cnf
  owner: root:root
  permissions: '0644'
- content: |
   {mysql_setup}
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
           port=self.port,
           subscriptions=self.cluster.subscriptions,
           connect_to_list=connect_to_list,
           rsa_priv=rsa_priv,
           host_files=host_files,
           mysql_setup=self.mysql_setup.replace("\n","\n    "))

    def do_launch(self):
        """Do the initial, fast part of launching this node."""
        logger.info("%s: provisioning node", self)
        # Elastic Block Storage
        dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType(iops=self.iops, volume_type=self.volume_type)
        dev_sda1.size = self.storage
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1
        # NID
        self.nid = self.cluster.next_nid()
        logger.debug("%s: Assigned NID %s", self, self.nid)
        # Security Group
        sg = ec2regions[self.region].create_security_group('dbaas-cluster-{c}-node-{n}'.format(c=self.cluster.pk, n=self.nid),'Security group for '+str(self))
        self.security_group = sg.id
        ec2regions[self.region].authorize_security_group(
            group_id=sg.id,
            ip_protocol='tcp',
            cidr_ip='0.0.0.0/0',
            from_port=self.port,
            to_port=self.port)
        logger.debug("%s: Created Security Group %s (named %s) with port %s open", self, sg.id, sg.name, self.port)
        self.save()
        # EC2 Instance
        try:
            sgs = settings.EC2_REGIONS[self.region]['SECURITY_GROUPS'] + [sg.name]
        except KeyError:
            sgs = [sg.name]
        res = ec2regions[self.region].run_instances(
            settings.EC2_REGIONS[self.region]["AMI"],
            key_name=settings.EC2_REGIONS[self.region]['KEY_NAME'],
            instance_type=self.size,
            block_device_map=bdm,
            security_groups=sgs,
            user_data ='#include\nhttp://'+Site.objects.get_current().domain+self.get_absolute_url()+'cloud_config/',
        )
        self._instance = res.instances[0]
        self.instance_id = self.instance.id
        logger.debug("%s: Rservation %s launched. Instance id %s", self, res.id, self.instance_id)
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
            'url':'http://'+Site.objects.get_current().domain+self.get_absolute_url(),
        })
        r53 = boto.connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        health_check = HealthCheck(connection=r53, caller_reference=self.instance_id,
            ip_address=self.ip, port=self.port, health_check_type='TCP')
        self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
        rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE_ID)
        rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.cluster.lbr_dns_name,
            type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, region=self.region))
        rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
            resource_records=[self.ip]))
        rrs.commit()
        self.status = self.RUNNING
        self.save()
        #... wait until node has fetched config and installed and tests run...
        # self.status = self.RUNNING
        # self.save()

    def on_terminate(self):
        if self.status in (self.PROVISIONING, self.INSTALLING_CF, self.RUNNING, self.ERROR):
            logger.debug("%s: terminating instance %s", self, self.instance_id)
            r53 = boto.connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE_ID)
            rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.cluster.lbr_dns_name,
                type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, region=self.region))
            rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                resource_records=[self.ip]))
            rrs.commit()
            r53.delete_health_check(self.health_check)
            ec2regions[self.region].terminate_instances([self.instance_id])
            if self.security_group != "":
                self.status = self.SHUTTING_DOWN
                self.save()
                while self.shutting_down():
                    sleep(15)
                logger.debug("%s: terminating security group %s", self, self.security_group)
                ec2regions[self.region].delete_security_group(group_id=self.security_group)

@receiver(models.signals.pre_delete, sender=Node)
def node_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Node:
        return
    instance.on_terminate()
