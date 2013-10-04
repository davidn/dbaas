#!/usr/bin/python

"""Manage clusters of GenieDB nodes.

This module provides classes to create, manage and destroy clusters of GenieDB
nodes.  It consists of three related classes, Cluster, Node and
LBRRegionNodeSet. Each Cluster contains several Nodes; each cluster has
LBRRegionNodeSet which in turn contain Nodes, such that the LBRRegionNodeSets
partition the Nodes in a cluster. See `the wiki`_ for more info.

.. _the wiki: https://geniedb.atlassian.net/wiki/x/NgCYAQ

"""

from time import sleep
import re
from hashlib import sha1
from itertools import islice
import base64
import datetime
from Crypto import Random
from Crypto.PublicKey import RSA
import OpenSSL
from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.sites.models import Site
from logging import getLogger
from .route53 import RecordWithHealthCheck, RecordWithTargetHealthCheck, HealthCheck, record, exception
from boto import connect_route53, connect_s3, connect_iam
from .uuid_field import UUIDField
from .cloud import EC2, Rackspace, ProfitBrick, Cloud
import config
import MySQLdb
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from boto.exception import S3ResponseError
from pyzabbix import ZabbixAPI
import audit

logger = getLogger(__name__)

cronvalidators = (
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 59) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 23) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 1 <= int(x,10) <= 31) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 1 <= int(x,10) <= 12) or allowtext and x.lower() in ('*','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 07)or allowtext and x.lower() in ('*','mon','tue','wed','thu','fri','sat','sun')
)
"""Functions for validating each field of a cron schedule"""

def cron_validator(value):
    """Raise an error if :param value: is not a valid cron schedule."""
    if "\n" in value or "\r" in value:
        raise ValidationError("No new lines allowed in schedule")
    values = value.split()
    if len(values) != 5:
        raise ValidationError("Schedule must have exactly 5 whitespace separated fields")
    for period, field in enumerate(values):
        for part in field.split(","):
            part_step = part.split("/")
            if not 0 < len(part_step) <= 2:
                raise ValidationError("Invalid schedule step: %s" % part)
            part_range = part_step[0].split("-")
            if not 0 < len(part_range) <= 2:
                raise ValidationError("Invalid schedule range: %s" % part_step[0])
            if len(part_range) == 2:
                if not cronvalidators[period](part_range[0], False):
                    raise ValidationError("Invalid range part: %s" % part_range[0])
                if not cronvalidators[period](part_range[1], False):
                    raise ValidationError("Invalid range part: %s" % part_range[1])
            elif not cronvalidators[period](part_range[0], True):
                    raise ValidationError("Invalid range part: %s" % part_range[0])
            if len(part_step) > 1:
                if len(part_range) == 1 and part_range[0] != '*':
                    raise ValidationError("Schedule step requires a range to step over")
                if not re.match(r'^\d+$', part_step[1]):
                    raise ValidationError("Invalid step: %s" % part_step[1])

def split_every(n, iterable):
    """"Given an iterable, return slices of the iterable in separate lists."""
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def asn1_to_pem(s):
    return "-----BEGIN RSA PRIVATE KEY-----\n{0}-----END RSA PRIVATE KEY-----\n".format(base64.encodestring(s))

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_paid = models.BooleanField(_('paid'), default=False,
        help_text=_('Designates whether this user should be allowed to '
                    'create arbitrary nodes and clusters.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @models.permalink
    def get_absolute_url(self):
        return ('user-detail', [self.pk])

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

class Cluster(models.Model):
    """Manage a cluster.

    This cluster is a container for a group of nodes which are kept in sync
    by GenieDB. It also stores common properties, and is responsible for
    managing the space in which backups are stored.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clusters')

    uuid = UUIDField(primary_key=True)
    label = models.CharField(max_length=255, blank=True, default="")
    port = models.PositiveIntegerField("MySQL Port", default=settings.DEFAULT_PORT)
    dbname = models.CharField("Database Name", max_length=255)
    dbusername = models.CharField("Database Username", max_length=255)
    dbpassword = models.CharField("Database Password", max_length=255)
    backup_count = models.PositiveIntegerField("Number of backups to keep", default=24)
    backup_schedule = models.CharField("Cron-style backup schedule", max_length=255, validators=[cron_validator], default="3 */2 * * *")
    iam_arn = models.CharField(max_length=255, blank=True, default="")
    iam_key = models.CharField(max_length=255, blank=True, default="")
    iam_secret = models.CharField(max_length=255, blank=True, default="")

    # SSL Keys
    ca_cert = models.TextField("CA Certificate", blank=True, default="")
    client_cert = models.TextField("Client Certificate", blank=True, default="")
    server_cert = models.TextField("Server Certificate", blank=True, default="")
    client_key = models.TextField("Client Private Key", blank=True, default="")
    server_key = models.TextField("Server Private Key", blank=True, default="")

    historyTrail = audit.AuditTrail(show_in_admin=True)

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.dns_name

    def generate_keys(self):
        # idempotence
        if len(self.ca_cert) != 0:
            return
        ca_pk = OpenSSL.crypto.PKey()
        ca_pk.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        client_pk = OpenSSL.crypto.PKey()
        client_pk.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        server_pk = OpenSSL.crypto.PKey()
        server_pk.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        ca_cert = OpenSSL.crypto.X509()
        ca_cert.set_pubkey(ca_pk)
        ca_cert.get_subject().C = 'US'
        ca_cert.get_subject().ST = 'CA'
        ca_cert.get_subject().CN = 'GenieDB Inc.'
        ca_cert.set_issuer(ca_cert.get_subject())
        ca_cert.set_notBefore(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%SZ'))
        ca_cert.set_notAfter((datetime.datetime.utcnow()+datetime.timedelta(3650)).strftime('%Y%m%d%H%M%SZ'))
        ca_cert.set_serial_number(1)
        ca_cert.sign(ca_pk,'sha256')
        client_cert = OpenSSL.crypto.X509()
        client_cert.set_pubkey(client_pk)
        client_cert.get_subject().CN = str(self)
        client_cert.set_issuer(ca_cert.get_subject())
        client_cert.set_notBefore(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%SZ'))
        client_cert.set_notAfter((datetime.datetime.utcnow()+datetime.timedelta(3650)).strftime('%Y%m%d%H%M%SZ'))
        client_cert.set_serial_number(2)
        client_cert.sign(ca_pk,'sha256')
        server_cert = OpenSSL.crypto.X509()
        server_cert.set_pubkey(server_pk)
        server_cert.get_subject().C = 'US'
        server_cert.get_subject().ST = 'CA'
        server_cert.get_subject().O = 'GenieDB Inc.'
        server_cert.get_subject().CN = self.dns_name
        server_cert.set_issuer(ca_cert.get_subject())
        server_cert.set_notBefore(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%SZ'))
        server_cert.set_notAfter((datetime.datetime.utcnow()+datetime.timedelta(3650)).strftime('%Y%m%d%H%M%SZ'))
        server_cert.set_serial_number(3)
        server_cert.sign(ca_pk,'sha256')

        self.client_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, client_cert)
        self.server_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, server_cert)
        self.client_key = asn1_to_pem(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, client_pk))
        self.server_key = asn1_to_pem(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, server_pk))
        self.ca_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert)

    def launch(self):
        """Set up an IAM user and S3 bucket for nodes in this cluster to send backups to."""
        self.generate_keys()
        if self.iam_key == "":
            iam = connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            if self.iam_arn == "":
                res= iam.create_user(self.uuid)
                self.iam_arn = res['create_user_response']['create_user_result']['user']['arn']
                self.save()
            res = iam.create_access_key(self.uuid)
            self.iam_key = res['create_access_key_response']['create_access_key_result']['access_key']['access_key_id']
            self.iam_secret = res['create_access_key_response']['create_access_key_result']['access_key']['secret_access_key']
            self.save()
        s3 = connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        bucket = s3.lookup(self.uuid)
        if bucket is None:
            bucket = s3.create_bucket(self.uuid)
        # S3 takes a while to treat new ARN as valid
        for i in xrange(15):
            try:
                bucket.set_policy("""{
                  "Version": "2008-10-17",
                  "Id": "S3PolicyId1",
                  "Statement": [
                    {
                      "Sid": "IPAllow",
                      "Effect": "Allow",
                      "Principal": {
                        "AWS": "%(iam)s"
                      },
                      "Action": "s3:*",
                      "Resource": ["arn:aws:s3:::%(bucket)s","arn:aws:s3:::%(bucket)s/*"]
                }]}""" % {'iam':self.iam_arn, 'bucket':self.uuid})
                break
            except S3ResponseError as e:
                if i < 15:
                    logger.info("Retrying S3 permission grant.  Err='%s'" % (e.message))
                    sleep(2)
                else:
                    logger.info("Retry limit exceeded, error='%s'" % (e.message))
                    raise

    def terminate(self):
        """Clean up the S3 bucket and IAM user associated with this cluster."""
        s3 = connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        bucket = s3.lookup(self.uuid)
        if bucket is not None:
            # Must empty bucket before delete
            for keys in split_every(1000, bucket):
                bucket.delete_keys(keys)
            bucket.delete()
        if self.iam_arn != "":
            iam = connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            if self.iam_key != "":
                iam.delete_access_key(self.iam_key,self.uuid)
                self.iam_key = ""
                self.save()
            iam.delete_user(self.uuid)
            self.iam_arn = ""
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('cluster-detail', [self.pk])

    def next_nid(self):
        """Return the next available node id."""
        return max([node.nid for node in self.nodes.all()]+[0])+1

    @property
    def dns_name(self):
        return settings.CLUSTER_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.'+str(node.nid), "5502"]) for node in self.nodes.all())

    def get_lbr_region_set(self, region):
        """Given a Region object, return the LBRRegionNodeSet for that region in this cluster, creating one if needed."""
        obj, _ = self.lbr_regions.get_or_create(cluster=self.pk, lbr_region=region.lbr_region)
        return obj

def gen_private_key():
    """Generate a 2048 bit RSA key, exported as ASCII, suitable for use with tinc."""
    return RSA.generate(2048, Random.new().read).exportKey()

class Provider(models.Model):
    """Represent a Cloud Compute provider."""
    name = models.CharField("Name", max_length=255)
    code = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('provider-detail', [self.pk])

    def __unicode__(self):
        return self.name

class Region(models.Model):
    """Represent a region in a Cloud"""
    provider = models.ForeignKey(Provider, related_name='regions')
    code = models.CharField("Code", max_length=20)
    name = models.CharField("Name", max_length=255)
    image = models.CharField("Image", max_length=255)
    lbr_region = models.CharField("LBR Region", max_length=20)
    key_name = models.CharField("SSH Key", max_length=255)
    security_group = models.CharField("Security Group", max_length=255)
    longitude = models.FloatField("Longitude", validators=[MaxValueValidator(180), MinValueValidator(-180)])
    latitude = models.FloatField("Latitude", validators=[MaxValueValidator(90), MinValueValidator(-90)])

    @models.permalink
    def get_absolute_url(self):
        return ('region-detail', [self.pk])

    def __unicode__(self):
        return self.name

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            if self.provider.code == "az":
                self._connection = EC2(self)
            elif self.provider.code == "rs":
                self._connection = Rackspace(self)
            elif self.provider.code == "pb":
                self._connection = ProfitBrick(self)
            elif self.provider.code == "test":
                self._connection = Cloud(self)
            else:
                raise KeyError("Unknown provider '%s'" % self.provider.name)
        return self._connection

    def __getstate__(self):
        if hasattr(self,'_connection'):
            odict = self.__dict__.copy()
            del odict['_connection']
            return odict
        else:
            return self.__dict__

class Flavor(models.Model):
    """Represent a size/type of instance that can be created in a cloud"""
    provider = models.ForeignKey(Provider, related_name='flavors')
    code = models.CharField("Code", max_length=20)
    name = models.CharField("Name", max_length=255)
    ram = models.PositiveIntegerField("RAM (MiB)")
    cpus = models.PositiveSmallIntegerField("CPUs")
    free_allowed = models.BooleanField("Free users allowed", default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('flavor-detail', [self.pk])

    def __unicode__(self):
        return self.name

class LBRRegionNodeSet(models.Model):
    """A set of Nodes in a cluster in the same DNS routing region

    See `the wiki`_ for more info.

    .. _the wiki: https://geniedb.atlassian.net/wiki/x/NgCYAQ

    """
    cluster = models.ForeignKey(Cluster, related_name='lbr_regions')
    lbr_region = models.CharField("LBR Region", max_length=20)
    launched = models.BooleanField("Launched")

    historyTrail = audit.AuditTrail(show_in_admin=True)

    def __unicode__(self):
        return self.dns_name

    @property
    def dns_name(self):
        return settings.REGION_DNS_TEMPLATE.format(cluster=self.cluster.pk, lbr_region=self.lbr_region)

    def do_launch(self):
        logger.debug("%s: setting up dns for lbr region %s, cluster %s", self, self.lbr_region, self.cluster.pk)
        if self.lbr_region != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('CREATE', self.record)
            rrs.commit()
        self.launched = True
        self.save()

    @property
    def identifier(self):
        return "%s-%s" % (self.cluster.pk, self.lbr_region)

    @property
    def record(self):
        return RecordWithTargetHealthCheck(name=self.cluster.dns_name,
            type='A', ttl=60, alias_hosted_zone_id=settings.ROUTE53_ZONE, alias_dns_name=self.dns_name,
            identifier=self.identifier, region=self.lbr_region)

    def on_terminate(self):
        logger.debug("%s: terminating dns for lbr region %s, cluster %s", self, self.lbr_region, self.cluster.pk)
        if self.lbr_region != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('DELETE', self.record)
            try:
                rrs.commit()
            except exception.DNSServerError, e:
                if re.search('but it was not found', e.body) is None:
                    raise
                else:
                    logger.warning("%s: terminating dns for lbr region %s, cluster %s skipped as record not found", self, self.lbr_region, self.cluster.pk)

class Node(models.Model):
    """Manage an individual instance in the cloud.

    Each node has a Cloud instance, and two DNS entries. This class is
    responsible for setting these up, including passing node-specific
    data to newly created instances.

    """
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
        (PROVISIONING, 'Provisioning Instances'),
        (INSTALLING_CF, 'Installing GenieDB CloudFabric'),
        (RUNNING, 'running'),
        (PAUSED, 'paused'),
        (SHUTTING_DOWN, 'shutting down'),
        (OVER, 'over'),
        (ERROR, 'An error occurred')
    )
    label = models.CharField(max_length=255, blank=True, default="")
    cluster = models.ForeignKey(Cluster, related_name='nodes')
    region = models.ForeignKey(Region, related_name='nodes')
    flavor = models.ForeignKey(Flavor, related_name='nodes')
    lbr_region = models.ForeignKey(LBRRegionNodeSet, related_name='nodes')
    instance_id = models.CharField("Instance ID", max_length=200, default="", blank=True)
    security_group = models.CharField("Security Group ID", max_length=200, default="", blank=True)
    health_check = models.CharField("R53 Health Check ID", max_length=200, default="", blank=True)
    nid = models.IntegerField("Node ID", default=None, blank=True, null=True)
    storage = models.IntegerField("Allocated Storage")
    ip = models.IPAddressField("Instance IP Address", default="", blank=True)
    iops = models.IntegerField("Provisioned IOPS", default=None, blank=True, null=True)
    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    tinc_private_key = models.TextField("Tinc Private Key", default=gen_private_key)

    historyTrail = audit.AuditTrail(show_in_admin=True)

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
        return "Node(pk={pk}, cluster={cluster}, flavor={flavor}, storage={storage}, region={region}{optional})".format(
            pk=repr(self.pk),
            cluster=repr(self.cluster),
            flavor=repr(self.flavor),
            storage=repr(self.storage),
            region=repr(self.region),
            optional=optional
        )

    def __unicode__(self):
        return self.dns_name

    def pending(self):
        """Return True if the instance is still being provisioned by the underlying cloud provider."""
        return self.region.connection.pending(self)

    def shutting_down(self):
        """Return True if the underlying cloud provider is in the process of shutting down the instance."""
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
    def customerName(self):
        return self.cluster.user.email

    def visible_name(self, labelText):
        return "{customerName}-{label}-{node}".format(customerName=self.customerName, label=labelText, node=self.nid)

    @property
    def public_key(self):
        return RSA.importKey(self.tinc_private_key).publickey().exportKey()

    @property
    def buffer_pool_size(self):
        return int(max(self.flavor.ram*0.7, self.flavor.ram-2048)*2**20)

    @property
    def cloud_config(self):
        """Return a string to be passed to cloud-init on a newly provisioned node."""
        connect_to_list = "\n    ".join("ConnectTo = node_"+str(node.nid) for node in self.cluster.nodes.all())
        rsa_priv = self.tinc_private_key.replace("\n", "\n    ")
        ca_cert = self.cluster.ca_cert.replace("\n", "\n   ")
        server_cert = self.cluster.server_cert.replace("\n", "\n   ")
        server_key = self.cluster.server_key.replace("\n", "\n   ")
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
    ssl_ca=/etc/mysql/ca.cert
    ssl_cert=/etc/mysql/server.cert
    ssl_key=/etc/mysql/server.pem
  path: /etc/mysql/conf.d/geniedb.cnf
  owner: root:root
  permissions: '0644'
- content: |
   {ca_cert}
  path: /etc/mysql/ca.cert
  permissions: '600'
  owner: mysql:mysql
- content: |
   {server_cert}
  path: /etc/mysql/server.cert
  permissions: '600'
  owner: mysql:mysql
- content: |
   {server_key}
  path: /etc/mysql/server.pem
  permissions: '600'
  owner: mysql:mysql
- content: |
   CREATE DATABASE {dbname};
   CREATE USER '{dbusername}'@'%' IDENTIFIED BY PASSWORD '{dbpassword}';
   CREATE USER '{mysql_user}'@'%' IDENTIFIED BY PASSWORD '{mysql_password}';
   GRANT ALL ON {dbname}.* to '{dbusername}'@'%';
   GRANT ALL ON *.* to '{mysql_user}'@'%' WITH GRANT OPTION;
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
    PidFile=/var/run/zabbix/zabbix_agentd.pid
    LogFile=/var/log/zabbix/zabbix_agentd.log
    LogFileSize=0
    Server=zabbix.geniedb.com
    ServerActive=zabbix.geniedb.com
    Hostname={dns_name}
    Include=/etc/zabbix/zabbix_agentd.d/
    EnableRemoteCommands=1
  path: /etc/zabbix/zabbix_agentd.conf
  permissions: '0644'
  owner: root:root
- path: /etc/mysqlbackup.logrotate
  content: |
    compress
    /var/backup/mysqlbackup.sql {{
        dateext
        dateformat -%Y%m%d.%s
        rotate {backup_count}
    }}
  owner: root:root
  permissions: '0644'
- path: /etc/cron.d/backup
  content: |
    {backup_schedule} root /usr/local/bin/backup
  owner: root:root
  permissions: '0644'
- path: /root/.s3cfg
  content: |
    access_key = {iam_key}
    secret_key = {iam_secret}
  owner: root:root
  permissions: '0600'
- path: /usr/local/bin/backup
  content: |
    #!/bin/sh
    /usr/bin/mysqldump --all-databases > /var/backup/mysqlbackup.sql
    /usr/sbin/logrotate -fs /etc/mysqlbackup.state /etc/mysqlbackup.logrotate
    /usr/bin/s3cmd sync --delete-removed /var/backup/ s3://{cluster}/{nid}/
    /usr/bin/curl {set_backup_url} -X POST -H "Content-type: application/json" -d "$(
      c=false
      cd /var/backup/
      printf '[\\n'
      for i in *; do
        if $c; then
          printf ',\\n'
        else
          c=true
        fi
        stat --printf '  {{"filename":"%n", "time":"%y", "size":"%s"}}' "$i"
      done
      printf '\\n]\\n'
    )"
  owner: root:root
  permissions: '0755'
- path: /etc/tinc/cf/rsa_key.priv
  owner: root:root
  permissions: '0600'
  content: |
    {rsa_priv}
{host_files}
runcmd:
- [lokkit, -p, "{port}:tcp"]
- [ mkdir, -p, /var/backup ]
""".format(nid=self.nid,
           dns_name=self.dns_name,
           cluster=self.cluster.pk,
           port=self.cluster.port,
           subscriptions=self.cluster.subscriptions,
           dbname=self.cluster.dbname,
           dbusername=self.cluster.dbusername,
           dbpassword='*'+sha1(sha1(self.cluster.dbpassword).digest()).hexdigest().upper(),
           mysql_user=settings.MYSQL_USER,
           mysql_password='*'+sha1(sha1(settings.MYSQL_PASSWORD).digest()).hexdigest().upper(),
           connect_to_list=connect_to_list,
           rsa_priv=rsa_priv,
           ca_cert=ca_cert,
           server_cert=server_cert,
           server_key=server_key,
           host_files=host_files,
           buffer_pool_size=self.buffer_pool_size,
           backup_schedule=self.cluster.backup_schedule.format(nid=self.nid),
           backup_count=self.cluster.backup_count,
           iam_key=self.cluster.iam_key,
           iam_secret=self.cluster.iam_secret,
           set_backup_url='https://'+Site.objects.get_current().domain+reverse('node-set-backups', args=[self.cluster.pk, self.pk]),
    )

    def addToHostGroup(self):
        hostName = self.dns_name
        logger.debug("%s.addToHostGroup: using customerName='%s', hostName='%s'" % (str(self), self.customerName, hostName))
        logger.debug("%s: visibleName='%s', ip='%s', label='%s'" % (str(self), self.visible_name(self.cluster.label), self.ip, self.cluster.label))
        # Be sure there is a HostGroup for the customerName so we can add a hostname to it
        # and add a hostname for the Node just launched.
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        tid = None
        gdbTemplates = z.template.getobjects(host='Template App GenieDB V2 Monitoring')
        if gdbTemplates:
            tid = gdbTemplates[0]['templateid']
        hostGroups = z.hostgroup.getobjects(name=self.customerName)
        if not hostGroups:
            try:
                z.hostgroup.create(name=self.customerName)
                logger.info("Created Zabbix HostGroup %s" % (self.customerName))
                hostGroups = z.hostgroup.getobjects(name=self.customerName)
            except:
                logger.warning("Failed to create Zabbix HostGroup %s" % (self.customerName))
        if not hostGroups:
            return
        zabbixHostGroup = hostGroups[0]
        try:
            if tid is not None:
                z.host.create(host=hostName, groups=[{"groupid":zabbixHostGroup["groupid"]}], name=self.visible_name(self.cluster.label),
                    interfaces={"type":'1', "main":'1', "useip":'1', "ip":self.ip, "dns":hostName, "port":"10050"},
                    templates={"templateid":tid})
            else:
                z.host.create(host=hostName, groups=[{"groupid":zabbixHostGroup["groupid"]}], name=self.visible_name(self.cluster.label),
                    interfaces={"type":'1', "main":'1', "useip":'1', "ip":self.ip, "dns":hostName, "port":"10050"})
            logger.info("Created Zabbix Host %s" % (hostName))
        except:
            logger.warning("Failed to create Zabbix Host %s" % (hostName))

    def removeFromHostGroup(self):
        hostName = self.dns_name
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        # Find the Zabbix HostGroup and Host IDs
        # then delete the Host node,
        # and if the HostGroup is now empty, remove it too.
        hostGroups = z.hostgroup.getobjects(name=self.customerName)
        if not hostGroups:
            return
        zabbixHostGroup = hostGroups[0]
        hosts = z.host.get(groupids=zabbixHostGroup["groupid"], output='extend')
        for zabbixHost in hosts:
            if zabbixHost['host'] == hostName:
                logger.info("Zabbix Host %s being removed." % (hostName))
                z.host.delete(hostid=zabbixHost['hostid'])
                hosts = z.host.get(groupids=zabbixHostGroup["groupid"], output='extend')
                break
        if not hosts:
            logger.info("Zabbix HostGroup %s being removed." % (self.customerName))
            try:
                z.hostgroup.delete(zabbixHostGroup["groupid"])
            except:
                logger.warning("Failed to delete Zabbix HostGroup %s" % (self.customerName))

    def do_launch(self):
        """Do the initial, fast part of launching this node."""
        assert(self.status != Node.OVER)
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
        assert(self.status != Node.OVER)
        while self.pending():
            sleep(15)
        self.update({
            'Name':'dbaas-cluster-{c}-node-{n}'.format(c=self.cluster.pk, n=self.nid),
            'username':self.cluster.user.email,
            'cluster':str(self.cluster.pk),
            'node':str(self.pk),
            'url':'https://'+Site.objects.get_current().domain+self.get_absolute_url(),
        })
        if self.region.provider.code != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            health_check = HealthCheck(connection=r53, caller_reference=self.instance_id,
                ip_address=self.ip, port=self.cluster.port, health_check_type='TCP')
            self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, weight=1))
            rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
                resource_records=[self.ip]))
            rrs.commit()
        self.status = self.RUNNING
        self.save()
        self.addToHostGroup()
        #... wait until node has fetched config and installed and tests run...
        # self.status = self.RUNNING
        # self.save()

    def pause(self):
        """Suspend this node."""
        assert(self.status == Node.RUNNING)
        self.region.connection.pause(self)
        self.status = Node.PAUSED
        self.save()

    def resume(self):
        """Resume this node."""
        assert(self.status == Node.PAUSED)
        self.region.connection.resume(self)
        self.status = Node.RUNNING
        self.save()

    def add_database(self, dbname):
        """Create a new MySQL database on this node and grant the user permission to it."""
        if len(dbname)>64:
            raise RuntimeError("Database name too long: %s" % dbname)
        if not re.match(r'^\w*[A-Za-z]\w*$', dbname):
            raise RuntimeError("Database name must consist of at least one letter and numbers only: %s" % dbname)
        con = MySQLdb.connect(host=self.dns_name,
                user=settings.MYSQL_USER,
                passwd=settings.MYSQL_PASSWORD,
                port=self.cluster.port)
        try:
            cur = con.cursor()
            try:
                try:
                    # Note we don't use real placeholder syntax as CREATE DATABASE fails
                    # if quotes are present
                    cur.execute("CREATE DATABASE IF NOT EXISTS " + dbname + ";")
                except Warning:
                    pass
                try:
                    cur.execute("GRANT ALL ON " + dbname + ".* to %s@'%%';", (self.cluster.dbusername,))
                except Warning:
                    pass
            finally:
                cur.close()
        finally:
            con.close()

    def on_terminate(self):
        """Shutdown the node and remove DNS entries."""
        self.removeFromHostGroup()
        if self.status in (self.PROVISIONING, self.INSTALLING_CF, self.RUNNING, self.PAUSED, self.ERROR):
            logger.debug("%s: terminating instance %s", self, self.instance_id)
            if self.region.provider.code != 'test':
                r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
                rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
                rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                    type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id, weight=1))
                rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                    resource_records=[self.ip]))
                rrs.commit()
                r53.delete_health_check(self.health_check)
            self.region.connection.terminate(self)

class Backup(models.Model):
    """A record of a backup."""
    node = models.ForeignKey(Node, related_name='backups')
    filename = models.CharField(max_length=255)
    time = models.DateTimeField()
    size = models.PositiveIntegerField("Backup size (MB)")

    def get_url(self):
        s3 = connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        return s3.generate_url(3600,
                "GET", self.node.cluster.uuid,
                '/%s/%s' % (self.node.nid, self.filename))

@receiver(models.signals.pre_delete, sender=Node)
def node_pre_delete_callback(sender, instance, using, **kwargs):
    """Terminate Nodes when the instances is deleted"""
    if sender != Node:
        return
    instance.on_terminate()

@receiver(models.signals.pre_delete, sender=LBRRegionNodeSet)
def region_pre_delete_callback(sender, instance, using, **kwargs):
    """Terminate LBRRegionNodeSets when the instances is deleted"""
    if sender != LBRRegionNodeSet:
        return
    instance.on_terminate()

@receiver(models.signals.pre_delete, sender=Cluster)
def cluster_pre_delete_callback(sender, instance, using, **kwargs):
    """Terminate Clusters when the instances is deleted"""
    if sender != Cluster:
        return
    instance.terminate()


