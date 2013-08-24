#!/usr/bin/python

from time import sleep
import re
from sha import sha
from itertools import islice
from Crypto import Random
from Crypto.PublicKey import RSA
from django.db import models
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from logging import getLogger
from .route53 import RecordWithHealthCheck, RecordWithTargetHealthCheck, HealthCheck, record, exception
from boto import connect_route53, connect_s3, connect_iam
from .uuid_field import UUIDField
from .cloud import EC2, Rackspace, Cloud
import config
import MySQLdb
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from boto.exception import S3ResponseError

logger = getLogger(__name__)

cronvalidators = (
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 59) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 23) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 1 <= int(x,10) <= 31) or allowtext and x == '*',
    lambda x, allowtext: (re.match(r'^\d+$',x) and 1 <= int(x,10) <= 12) or allowtext and x.lower() in ('*','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),
    lambda x, allowtext: (re.match(r'^\d+$',x) and 0 <= int(x,10) <= 07)or allowtext and x.lower() in ('*','mon','tue','wed','thu','fri','sat','sun')
)

def cron_validator(value):
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
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

class Cluster(models.Model):
    user = models.ForeignKey(User)
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

    def __repr__(self):
        return "Cluster(uuid={uuid}, user={user})".format(uuid=repr(self.uuid), user=repr(self.user))

    def __unicode__(self):
        return self.dns_name

    def launch(self):
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
                continue
            except S3ResponseError, e:
                if e.message == "Invalid principal in policy":
                    logger.info("Retrying S3 permission grant")
                    sleep(2)
                else:
                    raise

    def terminate(self):
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
        return max([node.nid for node in self.nodes.all()]+[0])+1

    @property
    def dns_name(self):
        return settings.CLUSTER_DNS_TEMPLATE.format(cluster=self.pk)

    @property
    def subscriptions(self):
        return ",".join(":".join([str(node.nid), '192.168.33.'+str(node.nid), "5502"]) for node in self.nodes.all())

    def get_lbr_region_set(self, region):
        obj, _ = self.lbr_regions.get_or_create(cluster=self.pk, lbr_region=region.lbr_region)
        return obj

def gen_private_key():
    return RSA.generate(2048, Random.new().read).exportKey()

class Provider(models.Model):
    name = models.CharField("Name", max_length=255)
    code = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('provider-detail', [self.pk])

    def __unicode__(self):
        return self.name

class Region(models.Model):
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
    provider = models.ForeignKey(Provider, related_name='flavors')
    code = models.CharField("Code", max_length=20)
    name = models.CharField("Name", max_length=255)
    ram = models.PositiveIntegerField("RAM (MiB)")
    cpus = models.PositiveSmallIntegerField("CPUs")

    @models.permalink
    def get_absolute_url(self):
        return ('flavor-detail', [self.pk])

    def __unicode__(self):
        return self.name

class LBRRegionNodeSet(models.Model):
    cluster = models.ForeignKey(Cluster, related_name='lbr_regions')
    lbr_region = models.CharField("LBR Region", max_length=20)
    launched = models.BooleanField("Launched")

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
                    logger.warning("%s: terminating dns for lbr region %s, cluster %s skipped as record not found")

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
    def public_key(self):
        return RSA.importKey(self.tinc_private_key).publickey().exportKey()

    @property
    def buffer_pool_size(self):
        return int(max(self.flavor.ram*0.7, self.flavor.ram-2048)*2**20)

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
           dbpassword='*'+sha(sha(self.cluster.dbpassword).digest()).hexdigest().upper(),
           mysql_user=settings.MYSQL_USER,
           mysql_password='*'+sha(sha(settings.MYSQL_PASSWORD).digest()).hexdigest().upper(),
           connect_to_list=connect_to_list,
           rsa_priv=rsa_priv,
           host_files=host_files,
           buffer_pool_size=self.buffer_pool_size,
           backup_schedule=self.cluster.backup_schedule.format(nid=self.nid),
           backup_count=self.cluster.backup_count,
           iam_key=self.cluster.iam_key,
           iam_secret=self.cluster.iam_secret,
           set_backup_url='https://'+Site.objects.get_current().domain+reverse('node-set-backups', args=[self.cluster.pk, self.pk]),
    )

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
        #... wait until node has fetched config and installed and tests run...
        # self.status = self.RUNNING
        # self.save()

    def pause(self):
        assert(self.status == Node.RUNNING)
        self.region.connection.pause(self)
        self.status = Node.PAUSED
        self.save()

    def resume(self):
        assert(self.status == Node.PAUSED)
        self.region.connection.resume(self)
        self.status = Node.RUNNING
        self.save()

    def add_database(self, dbname):
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
    if sender != Node:
        return
    instance.on_terminate()

@receiver(models.signals.pre_delete, sender=LBRRegionNodeSet)
def region_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != LBRRegionNodeSet:
        return
    instance.on_terminate()

@receiver(models.signals.pre_delete, sender=Cluster)
def cluster_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Cluster:
        return
    instance.terminate()
