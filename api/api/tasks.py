#!/usr/bin/python

from django.conf import settings
from logging import getLogger
from celery.task import Task, task
from time import sleep
from .models import Node, Cluster
import datetime
from django.dispatch.dispatcher import receiver
from django.db import models
from django.contrib.auth import get_user_model
from pyzabbix import ZabbixAPI
from api.exceptions import BackendNotReady, SaltError
from boto.route53.exception import DNSServerError
from boto.exception import BotoClientError, BotoServerError

logger = getLogger(__name__)

if hasattr(settings, 'BUGSNAG'):
    from celery.signals import after_setup_logger, after_setup_task_logger
    def add_logger(logger, *args, **kwargs):
        import bugsnag.handlers
        logger.addHandler(bugsnag.handlers.BugsnagHandler())
    after_setup_logger.connect(add_logger)
    after_setup_task_logger.connect(add_logger)

class NodeTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        args[0].status = Node.ERROR
        args[0].save()
        args[0].cluster.status = Cluster.ERROR
        args[0].cluster.save()

class ClusterTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        args[0].status = Cluster.ERROR
        args[0].save()

@task
def null_task():
    pass

# Tasks name <OBJECT>_<VERB>_<STEP>

@task(base=NodeTask)
def node_launch_provision(node):
    Node.objects.get(pk=node.pk).launch_async_provision()
@task(base=NodeTask, max_retries=40)
def node_launch_update(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_update()
    except BackendNotReady as e:
        node_launch_update.retry(exc=e, countdown=15)
@task(base=NodeTask, max_retries=10)
def node_launch_dns(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_dns()
    except DNSServerError as e:
        node_launch_dns.retry(exc=e, countdown=15)
@task(base=NodeTask, max_retries=10)
def node_launch_salt(node):
    try:
        Node.objects.get(pk=node.pk).launch_async_salt()
    except SaltError as e:
        if not e.missing:
            raise
        node_launch_salt.retry(exc=e, countdown=15)
@task(base=NodeTask)
def node_launch_zabbix(node):
    Node.objects.get(pk=node.pk).launch_async_zabbix()
@task(base=NodeTask)
def node_launch_complete(node):
    Node.objects.get(pk=node.pk).launch_complete()

@task()
def region_launch(region):
    region.launch_async()

@task(base=ClusterTask,max_retries=10)
def cluster_launch(cluster):
    try:
        Cluster.objects.get(pk=cluster.pk).launch_async()
    except (BotoClientError, BotoServerError) as e:
        cluster_launch.retry(exc=e, countdown=15)

@task(base=ClusterTask)
def cluster_launch_complete(cluster):
    Cluster.objects.get(pk=cluster.pk).launch_complete()

@task(base=ClusterTask)
def cluster_refresh_salt(cluster, *args):
    Cluster.objects.get(pk=cluster.pk).refresh_salt(*args)

@task()
def launch_email(cluster):
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
    cluster.user.email_user_template('confirmation_email', ctx_dict)

@task()
def send_reminder(user, reminder):
    if user.is_paid:
        return

    dictionary = {
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

    user.email_user_template(reminder['template'], ctx_dict)


@receiver(models.signals.post_save, sender=get_user_model())
def schedule_reminders(sender, instance, created, using, update_fields, **kwargs):
    if sender != get_user_model():
        return
    for reminder in getattr(settings, 'REMINDERS', ()):
        send_reminder.apply_async((instance, reminder), eta=reminder['ETA'])
