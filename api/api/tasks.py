#!/usr/bin/python

from django.conf import settings
from logging import getLogger
from celery.task import task
from celery import group
from time import sleep
from .models import Node
import datetime
from livesettings import config_value
from django.dispatch.dispatcher import receiver
from django.db import models
from django.contrib.auth import get_user_model
from pyzabbix import ZabbixAPI

logger = getLogger(__name__)


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
def wait_nodes_zabbix(cluster):
    nodes = cluster.nodes.all()

    z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
    z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    for node in nodes:
        hostName = node.dns_name
        key = "system.cpu.util[]"
        if node.region.provider.code != 'test':
            nodeIsReady = False
            for i in xrange(50):
                try:
                    items = z.item.get(host=hostName, filter={"key_": key})
                except:
                    logger.warning("Exception thrown trying to validate Zabbix registration for Host %s." % (hostName,))
                    break
                if items:
                    nodeIsReady = True
                    break
                logger.info("Trying to validate Zabbix registration for Host %s." % (hostName,))
                sleep(5)
            if not nodeIsReady:
                logger.warning("Unable to confirm that Host %s is executing before sending email notification." % (hostName,))



@task()
def launch_cluster(cluster):
    cluster.launch()

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
