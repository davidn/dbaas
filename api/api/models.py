#!/usr/bin/python

"""Manage clusters of GenieDB nodes.

This module provides classes to create, manage and destroy clusters of GenieDB
nodes.  It consists of three related classes, Cluster, Node and
LBRRegionNodeSet. Each Cluster contains several Nodes; each cluster has
LBRRegionNodeSet which in turn contain Nodes, such that the LBRRegionNodeSets
partition the Nodes in a cluster. See `the wiki`_ for more info.

.. _the wiki: https://geniedb.atlassian.net/wiki/x/NgCYAQ

"""

from logging import getLogger
from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.sites.models import Site
from .route53 import RecordWithHealthCheck, RecordWithTargetHealthCheck, HealthCheck, record, exception, catch_dns_exists, catch_dns_not_found
from boto import connect_route53, connect_s3, connect_iam
from .uuid_field import UUIDField
import providers
from .crypto import KeyPair, SslPair, CertificateAuthority
from .utils import retry, split_every, cron_validator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from pyzabbix import ZabbixAPI
from salt.client import LocalClient
from api.exceptions import BackendNotReady, check_for_salt_error


logger = getLogger(__name__)

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

    def email_user(self, subject, message, from_email=None, message_html=None):
        """
        Sends an email to this User.
        """
        from django.core.mail import EmailMultiAlternatives

        recipient = [settings.OVERRIDE_USER_EMAIL] if getattr(settings, 'OVERRIDE_USER_EMAIL', False) else [self.email]

        bcc_recipient = settings.INTERNAL_BCC_EMAIL if getattr(settings, 'INTERNAL_BCC_EMAIL', False) else None

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMultiAlternatives(subject, message, from_email, recipient, bcc=bcc_recipient)
        if message_html:
            msg.attach_alternative(message_html, "text/html")

        msg.send()

    def email_user_template(self, template_base_name, dictionary):
        """
        Sends a multipart html email to this User.
        """
        from django.template.loader import render_to_string

        subject = render_to_string(template_base_name + '_subject.txt', dictionary)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string(template_base_name + '.txt', dictionary)
        message_html = render_to_string(template_base_name + '.html', dictionary)

        self.email_user(subject, message_text, settings.DEFAULT_FROM_EMAIL, message_html)


class Cluster(models.Model):
    """Manage a cluster.

    This cluster is a container for a group of nodes which are kept in sync
    by GenieDB. It also stores common properties, and is responsible for
    managing the space in which backups are stored.

    """

    INITIAL = 0
    PROVISIONING = 3
    RUNNING = 6
    SHUTTING_DOWN = 7
    OVER = 8
    ERROR = 1000
    STATUSES = (
        (INITIAL, 'not yet started'),
        (PROVISIONING, 'Provisioning Instances'),
        (RUNNING, 'running'),
        (SHUTTING_DOWN, 'shutting down'),
        (OVER, 'over'),
        (ERROR, 'An error occurred')
    )
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

    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    history = HistoricalRecords()

    class Meta:
        unique_together=(("user","label"),)

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.dns_name

    def generate_keys(self):
        # idempotence
        if len(self.ca_cert) != 0:
            return
        ca = CertificateAuthority(CN='GenieDB Inc',ST='CA', C='US')
        client = SslPair(ca, CN=self.dns_name, O='GenieDB Inc',ST='CA', C='US')
        server = SslPair(ca, CN=self.dns_name, O='GenieDB Inc',ST='CA', C='US')
        self.client_cert = client.certificate
        self.client_key = client.private_key
        self.server_cert = server.certificate
        self.server_key = server.private_key
        self.ca_cert = ca.certificate

    def launch_sync(self):
        self.status = Cluster.PROVISIONING
        self.save()
    def launch_async(self):
        self.generate_keys()
        if self.iam_key == "":
            iam = connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            if self.iam_arn == "":
                res = iam.create_user(self.uuid)
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
        }]}""" % {'iam': self.iam_arn, 'bucket': self.uuid})
    def launch_complete(self):
        self.status = Cluster.RUNNING
        self.save()

    def refresh_salt(self, qs=None):
        if qs is None:
            qs = self.nodes.filter(status=Node.RUNNING)
        client = LocalClient()
        result = client.cmd([n.dns_name for n in qs], 'state.highstate',
                            expr_form='list', timeout=settings.SALT_TIMEOUT)
        check_for_salt_error(result, [n.dns_name for n in qs])

    def terminate(self):
        """Clean up the S3 bucket and IAM user associated with this cluster."""
        self.status = Cluster.SHUTTING_DOWN
        self.save()
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
                iam.delete_access_key(self.iam_key, self.uuid)
                self.iam_key = ""
                self.save()
            iam.delete_user(self.uuid)
            self.iam_arn = ""
            self.save()
        self.status = Cluster.OVER
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('cluster-detail', [self.pk])

    def next_nid(self):
        """Return the next available node id."""
        return max([node.nid for node in self.nodes.all()] + [0]) + 1

    @property
    def dns_name(self):
        return settings.CLUSTER_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.' + str(node.nid), "5502"]) for node in self.nodes.exclude(status__in=[Node.INITIAL, Node.OVER]))

    def get_lbr_region_set(self, region):
        """Given a Region object, return the LBRRegionNodeSet for that region in this cluster, creating one if needed."""
        obj, _ = self.lbr_regions.get_or_create(cluster=self.pk, lbr_region=region.lbr_region)
        return obj


def gen_private_key():
    """Generate a 2048 bit RSA key, exported as ASCII, suitable for use with tinc."""
    return KeyPair().private_key


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
    key_name = models.CharField("SSH Key", max_length=255, blank=True)
    security_group = models.CharField("Security Group", max_length=255, blank=True)
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
            self._connection = getattr(providers, self.provider.code)(self)
        return self._connection

    def __getstate__(self):
        if hasattr(self, '_connection'):
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

    history = HistoricalRecords()

    def __unicode__(self):
        return self.dns_name

    @property
    def dns_name(self):
        return settings.REGION_DNS_TEMPLATE.format(cluster=self.cluster.pk, lbr_region=self.lbr_region)

    def launch_async(self):
        logger.debug("%s: setting up dns for lbr region %s, cluster %s", self, self.lbr_region, self.cluster.pk)
        if self.lbr_region != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('CREATE', self.record)
            catch_dns_exists(rrs)
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
            def try_remove_dns():
                rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
                rrs.add_change_record('DELETE', self.record)
                catch_dns_not_found(rrs)
                return True
            retry(try_remove_dns)


class Node(models.Model):
    """Manage an individual instance in the cloud.

    Each node has a Cloud instance, and two DNS entries. This class is
    responsible for setting these up, including passing node-specific
    data to newly created instances.

    """
    INITIAL = 0
    STARTING = 12
    PROVISIONING = 3
    RUNNING = 6
    SHUTTING_DOWN = 7
    OVER = 8
    PAUSED = 9
    PAUSING = 10
    RESUMING = 11
    CONFIGURING_DNS = 14
    CONFIGURING_MONITORING = 13
    CONFIGURING_NODE = 15
    ERROR = 1000
    STATUSES = (
        (INITIAL, 'not yet started'),
        (STARTING, 'Starting launch'),
        (PROVISIONING, 'Provisioning Instances'),
        (CONFIGURING_DNS, 'configuring DNS'),
        (CONFIGURING_NODE, 'configuring node'),
        (CONFIGURING_MONITORING, 'configuring monitoring'),
        (RUNNING, 'running'),
        (PAUSED, 'paused'),
        (PAUSING, 'pausing'),
        (RESUMING, 'resuming'),
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

    history = HistoricalRecords()

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
    def public_key(self):
        return KeyPair(self.tinc_private_key).public_key

    @property
    def buffer_pool_size(self):
        return int(max(self.flavor.ram * 0.7, self.flavor.ram - 2048) * 2 ** 20)

    @property
    def set_backup_url(self):
        return 'https://' + Site.objects.get_current().domain + reverse('node-set-backups', args=[self.cluster.pk, self.pk])

    @property
    def customerName(self):
        return self.cluster.user.email

    def visible_name(self):
        return "{customerName}-{label}-{node}".format(customerName=self.customerName, label=self.cluster.label, node=self.nid)

    def addToHostGroup(self):
        hostName = self.dns_name
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        templates = z.template.getobjects(host='Template App GenieDB V2 Monitoring')
        if templates:
            logger.info("%s: Using zabbix template %s",
                        self, 'Template App GenieDB V2 Monitoring')
        else:
            logger.info("%s: Not using a zabbix template")

        hostGroups = z.hostgroup.getobjects(name=self.customerName)
        if not hostGroups:
            logger.info("%s: Creating Zabbix HostGroup %s", self, self.customerName)
            hostGroups = [{'groupid':gid} for gid in z.hostgroup.create(name=self.customerName)['groupids']]

        existingHosts = z.host.getobjects(name=self.visible_name())
        if existingHosts:
            logger.warning('%s: Cleaning up old zabbix host with same visible name "%s" and id "%s".',
                           self, self.visible_name(), existingHosts[0]['hostid'])
            z.host.delete(existingHosts[0])

        logger.info("%s: Creating Zabbix Host with visible name: %s", self, self.visible_name())
        z.host.create(host=hostName, groups=hostGroups, name=self.visible_name(), templates=templates,
                      interfaces={"type": '1', "main": '1', "useip": '1', "ip": self.ip, "dns": hostName, "port": "10050"})

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

    @property
    def health_check_reference(self):
        return str(self.id)+"-"+self.ip

    def setup_dns(self):
        if self.region.provider.code != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            health_check = HealthCheck(connection=r53, caller_reference=self.health_check_reference,
                                       ip_address=self.ip, port=self.cluster.port, health_check_type='TCP')
            try:
                self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
            except exception.DNSServerError, e:
                if e.status != 409:
                    raise
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                  type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id,
                                                                  weight=1))
            rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                          resource_records=[self.ip]))
            catch_dns_exists(rrs)

    def remove_dns(self):
        if self.region.provider.code != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                  type='A', ttl=60, resource_records=[self.ip], identifier=self.instance_id,
                                                                  weight=1))
            rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                          resource_records=[self.ip]))
            catch_dns_not_found(rrs)
            try:
                r53.delete_health_check(self.health_check)
            except exception.DNSServerError, e:
                if e.status != 404:
                    raise

    def assert_state(self, state, equal=True):
        assert equal == (self.status == state), \
            'Cannot launch node "%s" as it is in state %s.' % (self, dict(Node.STATUSES)[self.status])

    def launch_sync(self):
        self.assert_state(Node.OVER, False)
        self.nid = self.cluster.next_nid()
        logger.debug("%s: Assigned NID %s", self, self.nid)
        self.status = self.STARTING
        self.save()

    def launch_async_provision(self):
        self.status = self.PROVISIONING
        logger.info("%s: provisioning node", self)
        self.region.connection.launch(self)
        self.save()
        logger.info("%s: provisioning node done", self)

    def launch_async_update(self):
        self.assert_state(self.PROVISIONING)
        if self.pending():
            raise BackendNotReady()
        self.update({
            'Name': 'dbaas-cluster-{c}-node-{n}'.format(c=self.cluster.pk, n=self.nid),
            'username': self.cluster.user.email,
            'cluster': str(self.cluster.pk),
            'node': str(self.pk),
            'url': 'https://' + Site.objects.get_current().domain + self.get_absolute_url(),
        })
        self.save()

    def launch_async_dns(self):
        self.status = self.CONFIGURING_DNS
        self.save()
        self.setup_dns()
        self.save()

    def launch_async_salt(self):
        self.status = self.CONFIGURING_NODE
        self.refresh_salt()
        self.save()

    def launch_async_zabbix(self):
        self.status = self.CONFIGURING_MONITORING
        self.save()
        self.addToHostGroup()

    def launch_complete(self):
        self.status = self.RUNNING
        self.save()

    def refresh_salt(self):
        self.cluster.refresh_salt([self])

    def pause_sync(self):
        self.assert_state(Node.RUNNING)
        self.status = Node.PAUSING
        self.save()

    def pause_async(self):
        self.assert_state(Node.PAUSING)
        self.refresh_salt()
        self.status = Node.PAUSED
        self.save()

    def resume_sync(self):
        self.assert_state(Node.PAUSED)
        self.status = Node.RESUMING
        self.save()
    def resume_async(self):
        self.assert_state(Node.RESUMING)
        self.refresh_salt()
        self.status = Node.RUNNING
        self.save()

    def on_terminate(self):
        """Shutdown the node and remove DNS entries."""
        self.removeFromHostGroup()
        if self.status not in (self.INITIAL, self.OVER):
            logger.debug("%s: terminating instance %s", self, self.instance_id)
            self.remove_dns()
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

@receiver(models.signals.pre_save, sender=Node)
def node_pre_save_callback(sender, instance, raw, using, **kwargs):
    if sender != Node:
        return
    if raw:
        return
    instance.lbr_region = instance.cluster.get_lbr_region_set(instance.region)

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


