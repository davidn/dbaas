#!/usr/bin/python

from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from logging import getLogger
import boto.ec2

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

    def __repr__(self):
        return "Cluster(pk={pk}, user={user})".format(pk=repr(self.pk), user=repr(self.user))

    def __unicode__(self):
        return "Cluster {pk}".format(pk=self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('cluster-detail', [self.pk])

    def configuration(self):
        properties={
                'use_tinc': 'false',
                'netname': 'cf',
                'transport': 'tcp',
                'hosts_dir': settings.HOSTS_DIR+str(self.pk)}
        hosts = {}
        for node_id, node in enumerate(self.nodes.all(),1):
            hosts['node_{0}'.format(node_id)] = {
                'use_tinc': 'false',
                'netname': 'cf',
                'transport': 'tcp',
                'hosts_dir': settings.HOSTS_DIR+str(self.pk),
                'connect_to': node.dns,
                'number': node_id,
                'key': settings.EC2_REGIONS[node.region]['KEY_FILE']
            }
        return (properties, hosts)


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
    region = models.CharField("EC2 Region", max_length=20)
    size = models.CharField("Size", max_length=20)
    dns = models.CharField("EC2 Public DNS Address", max_length=200, default="", blank=True)
    ip = models.IPAddressField("EC2 Instance IP Address", default="", blank=True)
    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    cluster = models.ForeignKey(Cluster, related_name='nodes')

    def __repr__(self):
        optional = ""
        if self.instance_id != "":
            optional += ", instance_id={instance_id}".format(instance_id=repr(self.instance_id))
        if self.status != "":
            optional += ", status={status}".format(status=repr(self.status))
        if self.dns != "":
            optional += ", dns={dns}".format(dns=repr(self.dns))
        if self.ip != "":
            optional += ", ip={ip}".format(ip=repr(self.sip))
        return "Node(pk={pk}, cluster={cluster}, size={size}, region={region}{optional})".format(
            pk=repr(self.pk),
            cluster=repr(self.cluster),
            size=repr(self.size),
            region=repr(self.region),
            optional=optional
        )

    def __unicode__(self):
        if len(self.dns) == 0:
            return "Node {id}".format(id=self.instance_id)
        else:
            return "Node {id} at {dns}".format(id=self.instance_id, dns=self.dns)

    def pending(self):
        return self.instance.update()=='pending'

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
    def instance(self):
        if not hasattr(self, '_instance'):
            self._instance = ec2regions[self.region].get_all_instances(instance_ids=[self.instance_id])[0].instances[0]
        return self._instance

    def do_launch(self):
        logger.info("%s: provisioning node", self)
        res = ec2regions[self.region].run_instances(
            settings.EC2_REGIONS[self.region]["AMI"],
            key_name=settings.EC2_REGIONS[self.region]['KEY_NAME'],
            instance_type=self.size,
            security_groups=settings.EC2_REGIONS[self.region]['SECURITY_GROUPS']
        )
        self._instance = res.instances[0]
        self.instance_id = self.instance.id
        self.status = self.PROVISIONING
        self.save()

    def do_install(self):
        from tailor.cloudfabric import Cloudfabric
        from argparse import ArgumentParser
        from time import sleep
        while self.pending():
            sleep(15)
        self.update({
            'Name':'dbaas-cluster-{c}-node-{n}'.format(c=self.cluster.pk, n=self.pk),
            'username':self.cluster.user.username,
            'cluster':str(self.cluster.pk),
            'node':str(self.pk),
            'url':'http://'+Site.objects.get_current().domain+self.get_absolute_url(),
        })
        logger.info("%s: installing cloudfabric", self)
        self.status = self.INSTALLING_CF
        self.save()
        parser = ArgumentParser()
        subparsers = parser.add_subparsers()
        Cloudfabric.setup_argparse(subparsers.add_parser('cloudfabric'))
        params = parser.parse_args(['cloudfabric','refresh'])
        properties, params.hosts = self.cluster.configuration()
        Cloudfabric(params, properties).run()
        logger.info("%s: cloudfabric installation complete", self)
        self.status = self.RUNNING
        self.save()

    def on_terminate(self):
        logger.debug("%s: terminating", self)
        if self.status in (self.PROVISIONING, self.INSTALLING_CF, self.RUNNING, self.ERROR):
            ec2regions[self.region].terminate_instances([self.instance_id])

@receiver(models.signals.pre_delete, sender=Node)
def node_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Node:
        return
    instance.on_terminate()
