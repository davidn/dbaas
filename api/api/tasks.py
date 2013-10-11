#!/usr/bin/python

from django.conf import settings
from logging import getLogger
from celery.task import task
from time import sleep
from .models import Cluster
import datetime
from django.dispatch.dispatcher import receiver
from django.db import models
from django.contrib.auth import get_user_model
from pyzabbix import ZabbixAPI
from django.core.mail import mail_admins
from celery import AsyncResult

logger = getLogger(__name__)

if hasattr(settings, 'BUGSNAG'):
    from celery.signals import after_setup_logger, after_setup_task_logger
    def add_logger(logger, *args, **kwargs):
        import bugsnag.handlers
        logger.addHandler(bugsnag.handlers.BugsnagHandler())
    after_setup_logger.connect(add_logger)
    after_setup_task_logger.connect(add_logger)

@task()
def install_node(node):
    for i in xrange(10, 0, -1):
        try:
            return node.do_install()
        except:
            if i == 1:
                node.status = node.ERROR
                node.save()
                raise
            else:
                logger.info("Retrying cloudfabric install")
                sleep(15)


@task()
def install_region(region):
    region.do_launch()


@task()
def wait_nodes(nodes):
    for node in nodes:
        while node.pending():
            sleep(15)

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
def error_email(task_id):
    result = AsyncResult(task_id)
    exc = result.get(propagate=False)
    mail_admins('Task Failure occured', 'Task: %s\nException: %s\n%s'%(task_id, exc, result.traceback))

@task()
def wait_zabbix(cluster):
    nodes = cluster.nodes.all()

    z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
    z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    for node in nodes:
        if node.region.provider.code == 'test':
            continue
        for _ in xrange(50):
            items = z.item.get(host=node.dns_name, filter={"key_": "system.cpu.util[]"})
            if items:
                break
            logger.info("Retrying Zabbix registration for Host %s." % (node.dns_name,))
            sleep(5)
        assert(items, "Unable to confirm that Host %s is executing before sending email notification." % (node.dns_name,))

@task()
def launch_cluster(cluster):
    cluster.launch()

@task()
def cluster_ready(cluster):
    cluster.status = Cluster.RUNNING
    cluster.save()

@task()
def complete_pause_node(node):
    while node.pausing():
        sleep(15)
    node.complete_pause()

@task()
def complete_resume_node(node):
    while node.resuming():
        sleep(15)
    node.complete_resume()

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
