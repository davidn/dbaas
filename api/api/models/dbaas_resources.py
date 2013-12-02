from __future__ import unicode_literals
from logging import getLogger
import json
from collections import Sequence
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.contrib.sites.models import Site
from boto import connect_s3, connect_iam
from pyzabbix import ZabbixAPI, ZabbixAPIException
from simple_history.models import HistoricalRecords
from salt_jobs.models import send_salt_cmd, get_highstate_result
from ..crypto import KeyPair, SslPair, CertificateAuthority
from ..utils import retry, cron_validator
from ..route53 import RecordWithHealthCheck, RecordWithTargetHealthCheck, HealthCheck, record, exception, \
    catch_dns_exists, catch_dns_not_found, connect_route53
from ..exceptions import BackendNotReady
from .uuid_field import UUIDField
from .cloud_resources import Region, Flavor

logger = getLogger(__name__)

BUCKET_NAME = getattr(settings, 'S3_BUCKET', 'dbaas-backups')


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
    dbusername = models.CharField("Database Username", max_length=255, validators=[MaxLengthValidator(16)])
    dbpassword = models.CharField("Database Password", max_length=255)
    backup_count = models.PositiveIntegerField("Number of backups to keep", default=24)
    backup_schedule = models.CharField("Cron-style backup schedule", max_length=255, validators=[cron_validator],
                                       default="3 */2 * * *")
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
        unique_together = (("user", "label"),)
        app_label = "api"

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.dns_name

    def generate_keys(self):
        # idempotency
        if len(self.ca_cert) != 0:
            return
        ca = CertificateAuthority(CN='GenieDB Inc', ST='CA', C='US')
        client = SslPair(ca, CN=self.dns_name, O='GenieDB Inc', ST='CA', C='US')
        server = SslPair(ca, CN=self.dns_name, O='GenieDB Inc', ST='CA', C='US')
        self.client_cert = client.certificate
        self.client_key = client.private_key
        self.server_cert = server.certificate
        self.server_key = server.private_key
        self.ca_cert = ca.certificate

    def launch_sync(self):
        self.status = Cluster.PROVISIONING
        self.save()

    def launch_async_iam(self):
        self.generate_keys()
        if self.iam_key == "":
            iam = connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            if self.iam_arn == "":
                res = iam.create_user(self.uuid)
                self.iam_arn = res['create_user_response']['create_user_result']['user']['arn']
                self.save()
            iam.put_user_policy(self.uuid, self.uuid, json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["s3:ListBucket"],
                        "Resource": "arn:aws:s3:::%s" % BUCKET_NAME,
                        "Condition": {"StringLike": {"s3:prefix": "%s/*" % self.uuid}}
                    },
                    {
                        "Effect": "Allow",
                        "Action": [
                            "s3:DeleteObject",
                            "s3:PutObject"],
                        "Resource": "arn:aws:s3:::%s/%s/*" % (BUCKET_NAME, self.uuid)
                    }
                ]
            }))
            res = iam.create_access_key(self.uuid)
            self.iam_key = res['create_access_key_response']['create_access_key_result']['access_key']['access_key_id']
            self.iam_secret = res['create_access_key_response']['create_access_key_result']['access_key'][
                'secret_access_key']
            self.save()

    def launch_async_zabbix(self):
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        host_groups = z.hostgroup.getobjects(name=self.user.email)
        if not host_groups:
            logger.info("%s: Creating Zabbix HostGroup %s", self, self.user.email)
            z.hostgroup.create(name=self.user.email)

    def launch_complete(self):
        self.status = Cluster.RUNNING
        self.save()

    def add_database_sync(self, dbname):
        self.dbname += ',' + dbname
        self.save()

    def refresh_salt(self, qs=None):
        if qs is None:
            qs = self.nodes.filter(status=Node.RUNNING)
        jid = send_salt_cmd([n.dns_name for n in qs], 'state.highstate')
        for n in qs:
            n.last_salt_jid = jid
            n.save()

    def on_terminate(self):
        """Clean up the S3 bucket and IAM user associated with this cluster."""
        self.status = Cluster.SHUTTING_DOWN
        self.save()
        if self.iam_arn != "":
            iam = connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
            if self.iam_key != "":
                iam.delete_access_key(self.iam_key, self.uuid)
                self.iam_key = ""
                self.save()
            iam.delete_user_policy(self.uuid, self.uuid)
            iam.delete_user(self.uuid)
            self.iam_arn = ""
            self.save()
        self.status = Cluster.OVER
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return 'cluster-detail', [self.pk]

    def next_nid(self):
        """Return the next available node id."""
        return max([node.nid for node in self.nodes.all()] + [0]) + 1

    @property
    def dns_name(self):
        return settings.CLUSTER_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.' + str(node.nid), "5502"]) for node in
                        self.nodes.exclude(status__in=[Node.INITIAL, Node.OVER]))

    def get_lbr_region_set(self, region):
        """
        Given a Region object, return the LBRRegionNodeSet for that region in this cluster, creating one if needed.
        """
        obj, _ = self.lbr_regions.get_or_create(cluster=self.pk, lbr_region=region.lbr_region)
        return obj


class LBRRegionNodeSet(models.Model):
    """A set of Nodes in a cluster in the same DNS routing region

    See `the wiki`_ for more info.

    .. _the wiki: https://geniedb.atlassian.net/wiki/x/NgCYAQ

    """
    cluster = models.ForeignKey(Cluster, related_name='lbr_regions')
    lbr_region = models.CharField("LBR Region", max_length=20)
    launched = models.BooleanField("Launched", default=False)

    history = HistoricalRecords()

    class Meta:
        app_label = "api"

    def __unicode__(self):
        return self.dns_name

    @property
    def dns_name(self):
        return settings.REGION_DNS_TEMPLATE.format(cluster=self.cluster.pk, lbr_region=self.lbr_region)

    def launch_async(self):
        logger.debug("%s: setting up dns for lbr region %s, cluster %s", self, self.lbr_region, self.cluster.pk)
        if self.lbr_region != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY)
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
                                           type='A', ttl=60, alias_hosted_zone_id=settings.ROUTE53_ZONE,
                                           alias_dns_name=self.dns_name,
                                           identifier=self.identifier, region=self.lbr_region)

    def on_terminate(self):
        logger.debug("%s: terminating dns for lbr region %s, cluster %s", self, self.lbr_region, self.cluster.pk)
        if self.lbr_region != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY)

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
        (CONFIGURING_DNS, 'Configuring DNS'),
        (CONFIGURING_NODE, 'Configuring node'),
        (CONFIGURING_MONITORING, 'Configuring performance monitor'),
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
    storage = models.PositiveIntegerField("Storage", null=True, default=None, blank=True) # null = instance storage
    ip = models.IPAddressField("Instance IP Address", default="", blank=True)
    iops = models.IntegerField("Provisioned IOPS", default=None, blank=True, null=True)
    status = models.IntegerField("Status", choices=STATUSES, default=INITIAL)
    tinc_private_key = models.TextField("Tinc Private Key", blank=True)
    last_salt_jid = models.CharField(max_length=255, blank=True, default="")

    history = HistoricalRecords()

    class Meta:
        app_label = "api"

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

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.storage and not self.flavor.variable_storage_available:
            raise ValidationError("Instance type '%s' does not support variable storage." % self.flavor.code)
        if not self.storage and not self.flavor.fixed_storage:
            raise ValidationError("Instance type '%s' does not support fixed storage." % self.flavor.code)

    def pending(self):
        """Return True if the instance is still being provisioned by the underlying cloud provider."""
        return self.region.connection.pending(self)

    def shutting_down(self):
        """Return True if the underlying cloud provider is in the process of shutting down the instance."""
        return self.region.connection.shutting_down(self)

    def reinstantiating(self):
        """Return True if the underlying cloud provider is in the process of reinstantiating the instance."""
        return self.region.connection.reinstantiating(self)

    def update(self, tags=None):
        if tags is None:
            tags = {}
        return self.region.connection.update(self, tags)

    def get_ip(self):
        return self.region.connection.get_ip(self)

    @models.permalink
    def get_absolute_url(self):
        return 'node-detail', [self.cluster.pk, self.pk]

    @property
    def dns_name(self):
        return settings.NODE_DNS_TEMPLATE.format(cluster=self.cluster.pk, node=self.nid)

    @property
    def public_key(self):
        return KeyPair(self.tinc_private_key).public_key

    @property
    def buffer_pool_size(self):
        return int(max((self.flavor.ram - 128) * settings.BUFFER_POOL_PROPORTION, self.flavor.ram - 2048) * 2 ** 20)

    @property
    def set_backup_url(self):
        return 'https://' + Site.objects.get_current().domain + reverse('backup-list', args=[self.cluster.pk, self.pk])

    def visible_name(self):
        return "{email}-{label}-{node}".format(email=self.cluster.user.email, label=self.cluster.label, node=self.nid)

    def add_to_host_group(self):
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        templates = z.template.getobjects(host='Template App GenieDB V2 Monitoring')
        if templates:
            logger.info("%s: Using zabbix template %s",
                        self, 'Template App GenieDB V2 Monitoring')
        else:
            logger.info("%s: Not using a zabbix template")
        host_groups = z.hostgroup.getobjects(name=self.cluster.user.email)
        existing_hosts = z.host.getobjects(name=self.visible_name())
        if existing_hosts:
            logger.warning('%s: Cleaning up old zabbix host with same visible name "%s" and id "%s".',
                           self, self.visible_name(), existing_hosts[0]['hostid'])
            z.host.delete(existing_hosts[0])

        logger.info("%s: Creating Zabbix Host with visible name: %s", self, self.visible_name())
        z.host.create(host=self.dns_name, groups=host_groups, name=self.visible_name(), templates=templates,
                      interfaces={"type": '1', "main": '1', "useip": '1', "ip": self.ip, "dns": self.dns_name,
                                  "port": "10050"})

    def zabbix_monitoring(self, enable=True):
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        hostids = z.host.get(filter={'host': self.dns_name})
        assert (len(hostids) == 1)
        status = 0 if enable else 1
        z.host.update({'hostid': hostids[0]['hostid'], 'status': status})

    def remove_from_host_group(self):
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        # Find the Zabbix HostGroup and Host IDs
        # then delete the Host node,
        # and if the HostGroup is now empty, remove it too.
        host_groups = z.hostgroup.getobjects(name=self.cluster.user.email)
        if not host_groups:
            return
        zabbix_host_group = host_groups[0]
        hosts = z.host.get(groupids=zabbix_host_group["groupid"], output='extend')
        for zabbixHost in hosts:
            if zabbixHost['host'] == self.dns_name:
                logger.info("Zabbix Host %s being removed.", self.dns_name)
                z.host.delete(hostid=zabbixHost['hostid'])
                hosts = z.host.get(groupids=zabbix_host_group["groupid"], output='extend')
                break
        if not hosts:
            logger.info("Zabbix HostGroup %s being removed.", self.cluster.user.email)
            try:
                z.hostgroup.delete(zabbix_host_group["groupid"])
            except ZabbixAPIException:
                logger.warning("Failed to delete Zabbix HostGroup %s", self.cluster.user.email)

    @property
    def health_check_reference(self):
        return str(self.cluster.pk) + str(self.id) + "-" + self.ip

    def setup_dns(self):
        if self.region.provider.code != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY)
            health_check = HealthCheck(connection=r53, caller_reference=self.health_check_reference,
                                       ip_address=self.ip, port=self.cluster.port, health_check_type='TCP')
            self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                  type='A', ttl=60, resource_records=[self.ip],
                                                                  identifier=self.instance_id,
                                                                  weight=1))
            rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                          resource_records=[self.ip]))
            catch_dns_exists(rrs)

    def remove_dns(self):
        if self.region.provider.code != 'test':
            r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY)
            rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
            rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                  type='A', ttl=60, resource_records=[self.ip],
                                                                  identifier=self.instance_id,
                                                                  weight=1))
            rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                          resource_records=[self.ip]))
            catch_dns_not_found(rrs)
            try:
                r53.delete_health_check(self.health_check)
            except exception.DNSServerError, e:
                if e.status != 404:
                    raise

    def modify_dns(self, old_ip):
        if self.region.provider.code != 'test':
            # De-register the old address.
            # If the IP address didn't change then we don't need to do anything
            if old_ip and old_ip != self.ip:
                logger.info("Deregistering the old IP=%s to the new IP=%s" % (old_ip, self.ip))
                r53 = connect_route53(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                      aws_secret_access_key=settings.AWS_SECRET_KEY)

                # De-register the old IP address
                rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
                rrs.add_change_record('DELETE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                      type='A', ttl=60, resource_records=[old_ip],
                                                                      identifier=self.instance_id,
                                                                      weight=1))
                rrs.add_change_record('DELETE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                              resource_records=[old_ip]))
                catch_dns_not_found(rrs)

                try:
                    r53.delete_health_check(self.health_check)
                except exception.DNSServerError, e:
                    if e.status != 404:
                        raise

                # Now register the new IP address
                health_check = HealthCheck(connection=r53, caller_reference=self.health_check_reference,
                                           ip_address=self.ip, port=self.cluster.port, health_check_type='TCP')
                self.health_check = health_check.commit()['CreateHealthCheckResponse']['HealthCheck']['Id']
                rrs = record.ResourceRecordSets(r53, settings.ROUTE53_ZONE)
                rrs.add_change_record('CREATE', RecordWithHealthCheck(self.health_check, name=self.lbr_region.dns_name,
                                                                      type='A', ttl=60, resource_records=[self.ip],
                                                                      identifier=self.instance_id,
                                                                      weight=1))
                rrs.add_change_record('CREATE', record.Record(name=self.dns_name, type='A', ttl=3600,
                                                              resource_records=[self.ip]))
                catch_dns_exists(rrs)

    def assert_state(self, state, equal=True):
        if not isinstance(state, Sequence):
            state = (state,)
        assert equal == (self.status in state), \
            'Cannot launch node "%s" as it is in state %s.' % (self, dict(Node.STATUSES)[self.status])

    def generate_keys(self):
        # idempotence
        if len(self.tinc_private_key) != 0:
            return
        self.tinc_private_key = KeyPair().private_key

    def launch_sync(self):
        self.assert_state(Node.OVER, False)
        self.nid = self.cluster.next_nid()
        logger.debug("%s: Assigned NID %s", self, self.nid)
        self.status = self.STARTING
        self.save()

    def launch_async_provision(self):
        self.generate_keys()
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
        self.ip = self.get_ip()
        self.save()

    def launch_async_dns(self):
        self.status = self.CONFIGURING_DNS
        self.save()
        self.setup_dns()
        self.save()

    def launch_async_salt(self):
        self.status = self.CONFIGURING_NODE
        self.save()
        get_highstate_result(id=self.dns_name)

    def launch_async_zabbix(self):
        self.status = self.CONFIGURING_MONITORING
        self.save()
        self.add_to_host_group()

    def launch_complete(self):
        self.status = self.RUNNING
        self.save()

    def refresh_salt(self):
        self.cluster.refresh_salt([self])

    def refresh_salt_complete(self):
        get_highstate_result(id=self.dns_name, jid=self.last_salt_jid)

    def reinstantiate_sync(self, new_flavor):
        if self.status == self.INITIAL:
            self.flavor = new_flavor
            self.save()
            return False
        self.assert_state([Node.RUNNING, Node.PAUSED])
        if self.flavor.provider == new_flavor.provider \
                and self.flavor.code != new_flavor.code:
            self.flavor = new_flavor
            self.status = self.PROVISIONING
            self.save()
            return True
        return False

    def reinstantiate_async_setup(self):
        """Reinstantiate the node using its current flavor settings."""
        self.assert_state(Node.PROVISIONING)
        self.region.connection.reinstantiate_setup(self)

    def reinstantiate_async(self):
        """This part of the operation can be retried"""
        self.region.connection.reinstantiate(self)

    def reinstantiate_update(self):
        self.assert_state(self.PROVISIONING)
        if self.reinstantiating():
            raise BackendNotReady()
        old_ip = self.ip
        self.ip = self.get_ip()
        self.modify_dns(old_ip)
        self.save()

    def reinstantiate_complete(self):
        if self.reinstantiating():
            raise BackendNotReady()
        self.region.connection.reinstantiation_complete(self)
        self.status = self.RUNNING
        self.save()

    def pause_sync(self):
        self.assert_state(Node.RUNNING)
        self.status = Node.PAUSING
        self.save()

    def pause_async_salt(self):
        self.assert_state(Node.PAUSING)
        self.zabbix_monitoring(False)
        self.refresh_salt()

    def pause_complete(self):
        self.assert_state(Node.PAUSING)
        self.refresh_salt_complete()
        self.status = Node.PAUSED
        self.save()

    def resume_sync(self):
        self.assert_state(Node.PAUSED)
        self.status = Node.RESUMING
        self.save()

    def resume_async_salt(self):
        self.assert_state(Node.RESUMING)
        self.refresh_salt()

    def resume_complete(self):
        self.assert_state(Node.RESUMING)
        self.refresh_salt_complete()
        self.zabbix_monitoring(True)
        self.status = Node.RUNNING
        self.save()

    def on_terminate(self):
        """Shutdown the node and remove DNS entries."""
        self.remove_from_host_group()
        if self.status not in (self.INITIAL, self.OVER):
            logger.debug("%s: terminating instance %s", self, self.instance_id)
            self.remove_dns()
            self.region.connection.terminate(self)
        self.status = Node.OVER
        self.save()


class Backup(models.Model):
    """A record of a backup."""
    node = models.ForeignKey(Node, related_name='backups')
    filename = models.CharField(max_length=255)
    time = models.DateTimeField()
    size = models.BigIntegerField("Backup size (bytes)", validators=[MinValueValidator(0)])

    def __unicode__(self):
        return "%s backup of %s" % (self.time, self.node.dns_name)

    class Meta:
        app_label = "api"

    def get_url(self):
        s3 = connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        return s3.generate_url(3600,
                               "GET", BUCKET_NAME,
                               '%s/%s/%s' % (self.node.cluster.uuid, self.node.nid, self.filename))
