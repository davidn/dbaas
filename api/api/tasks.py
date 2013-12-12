#!/usr/bin/python

from __future__ import unicode_literals
import datetime
from logging import getLogger
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from boto.route53.exception import DNSServerError
from boto.exception import BotoClientError, BotoServerError
from celery.task import Task, task
from .models import Node, Cluster, Rule
from .exceptions import BackendNotReady

logger = getLogger(__name__)

if hasattr(settings, 'BUGSNAG'):
    import bugsnag.celery
    bugsnag.celery.connect_failure_handler()

class NodeTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        args[0].status = Node.ERROR
        args[0].save(update_fields=['status'])
        args[0].cluster.status = Cluster.ERROR
        args[0].cluster.save(update_fields=['status'])

class ClusterTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        args[0].status = Cluster.ERROR
        args[0].save(update_fields=['status'])

@task
def null_task():
    pass

# Tasks name <OBJECT>_<VERB>_<STEP>

@task(base=NodeTask)
def node_launch_provision(node):
    Node.objects.get(pk=node.pk).launch_async_provision()
@task(base=NodeTask, max_retries=90)
def node_launch_update(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_update()
    except BackendNotReady as e:
        node_launch_update.retry(exc=e, countdown=20)
@task(base=NodeTask, max_retries=10)
def node_launch_dns(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_dns()
    except DNSServerError as e:
        node_launch_dns.retry(exc=e, countdown=15)
@task(base=NodeTask, max_retries=30)
def node_launch_salt(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_salt()
    except ObjectDoesNotExist as e:
        node_launch_salt.retry(exc=e, countdown=15)
@task(base=NodeTask)
def node_launch_zabbix(node):
    Node.objects.get(pk=node.pk).launch_async_zabbix()
@task(base=NodeTask)
def node_launch_complete(node):
    Node.objects.get(pk=node.pk).launch_complete()

@task(base=NodeTask)
def node_pause_salt(node):
    Node.objects.get(pk=node.pk).pause_async_salt()
@task(base=NodeTask)
def node_pause_complete(node):
    try:
        Node.objects.get(pk=node.pk).pause_complete()
    except ObjectDoesNotExist, e:
        node_pause_complete.retry(exc=e, countdown=15)
@task(base=NodeTask)
def node_resume_salt(node):
    Node.objects.get(pk=node.pk).resume_async_salt()
@task(base=NodeTask, max_retries=30)
def node_resume_complete(node):
    try:
        Node.objects.get(pk=node.pk).resume_complete()
    except ObjectDoesNotExist, e:
        node_resume_complete.retry(exc=e, countdown=15)

@task(max_retries=10)
def region_launch(region):
    try:
        region.launch_async()
    except DNSServerError as e:
        region_launch.retry(exc=e,countdown=5)

@task(base=ClusterTask,max_retries=10)
def cluster_launch_iam(cluster):
    try:
        Cluster.objects.get(pk=cluster.pk).launch_async_iam()
    except (BotoClientError, BotoServerError) as e:
        cluster_launch_iam.retry(exc=e, countdown=15)
@task(base=ClusterTask)
def cluster_launch_zabbix(cluster):
    Cluster.objects.get(pk=cluster.pk).launch_async_zabbix()
@task(base=ClusterTask)
def cluster_launch_complete(cluster):
    Cluster.objects.get(pk=cluster.pk).launch_complete()

@task(base=NodeTask)
def node_reinstantiate_setup(node):
    Node.objects.get(pk=node.pk).reinstantiate_async_setup()
@task(base=NodeTask,max_retries=10)
def node_reinstantiate(node):
    try:
        Node.objects.get(pk=node.pk).reinstantiate_async()
    except () as e:
        node_reinstantiate.retry(exc=e, countdown=15)
@task(base=NodeTask,max_retries=180)    # This supports a max of 3 hrs!
def node_reinstantiate_update(node):
    try:
        Node.objects.get(pk=node.pk).reinstantiate_update()
    except BackendNotReady as e:
        node_reinstantiate_update.retry(exc=e, countdown=60)
@task(base=NodeTask,max_retries=20)
def node_reinstantiate_complete(node):
    try:
        Node.objects.get(pk=node.pk).reinstantiate_complete()
    except BackendNotReady as e:
        node_reinstantiate_complete.retry(exc=e, countdown=15)

@task(base=ClusterTask)
def cluster_refresh_salt(cluster, *args):
    Cluster.objects.get(pk=cluster.pk).refresh_salt(*args)
@task(base=NodeTask, max_retries=30)
def node_refresh_complete(node):
    try:
        Node.objects.get(pk=node.pk).refresh_salt_complete()
    except ObjectDoesNotExist, e:
        node_refresh_complete.retry(exc=e, countown=15)

@task(base=ClusterTask)
def cluster_shutdown(cluster):
    cluster.shutdown_async()

@task(base=NodeTask)
def node_shutdown_zabbix(node):
    node.shutdown_async_zabbix()
@task(base=NodeTask)
def node_shutdown_dns(node):
    node.shutdown_async_dns()
@task(base=NodeTask)
def node_shutdown_instance(node):
    node.shutdown_async_instance()
@task(base=NodeTask)
def node_shutdown_complete(node):
    node.shutdown_complete()

@task()
def launch_email(cluster, email_message='confirmation_email'):
    nodes = cluster.nodes.all()
    ctx_dict = {
        'nodes': nodes,
        'username': str(cluster.user),
        'is_paid': cluster.user.is_paid,
        'cluster_dns': cluster.dns_name,
        'trial_end': datetime.date.today() + settings.TRIAL_LENGTH,
        'port': cluster.port,
        'db': cluster.dbname,
        'dbusername': cluster.dbusername,
        'dbpassword': cluster.dbpassword,
        'regions': ' and '.join(node.region.name for node in nodes)
    }
    cluster.user.email_user_template(email_message, ctx_dict)

@task()
def rules_process():
    Rule.process()
