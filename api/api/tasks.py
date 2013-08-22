#!/usr/bin/python

from django.core.mail import EmailMultiAlternatives
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

logger = getLogger(__name__)

@task()
def install(node):
    for i in xrange(10,0,-1):
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
            sleep (15)

def node_text(node):
    return config_value('api_email','PLAINTEXT_PER_NODE').format(
       nid = node.nid,
       region = node.region.name,
       node_dns = node.dns_name,
       node_ip = node.ip
    )

def node_html(node):
    return config_value('api_email','HTML_PER_NODE').format(
       nid = node.nid,
       region = node.region.name,
       node_dns = node.dns_name,
       node_ip = node.ip
    )

def ordinal(num):
    if 4 <= num <= 20 or 24 <= num <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][num % 10 - 1]

@task()
def launch_email(cluster):
    nodes = cluster.nodes.all()
    params = {
        'node_text': ''.join(node_text(node) for node in nodes),
        'node_html': ''.join(node_html(node) for node in nodes),
        'username': str(cluster.user),
        'cluster_dns': cluster.dns_name,
        'trial_end': datetime.date.today() + settings.TRIAL_LENGTH,
        'ord': ordinal((datetime.date.today() + settings.TRIAL_LENGTH).day),
        'port': cluster.port,
        'db': cluster.dbname,
        'dbusername': cluster.dbusername,
        'dbpassword': cluster.dbpassword
    }
    email = EmailMultiAlternatives(
        subject=config_value('api_email','SUBJECT'),
        body=config_value('api_email','PLAINTEXT').format(**params),
        from_email=config_value('api_email','SENDER'),
        to=config_value('api_email','RECIPIENTS')
    )
    email.attach_alternative(
        config_value('api_email','HTML').format(**params),
        "text/html"
    )
    email.send()

@task()
def launch_cluster(cluster):
    cluster.launch()

def install_cluster(cluster):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = launch_cluster.si(cluster) | wait_nodes.si([node for node in install_nodes]) | group([install.si(node) for node in install_nodes]) | group([install_region.si(lbr_region) for lbr_region in lbr_regions]) | launch_email.si(cluster)
    return task.delay()

@task()
def send_reminder(user, reminder):
    if user.is_paid:
        return
    email = EmailMultiAlternatives(
        subject=reminder['SUBJECT'],
        body=reminder['PLAINTEXT'],
        from_email=reminder['SENDER'],
        to=[user.email]
    )
    email.attach_alternative(
        reminder['HTML'],
        "text/html"
    )
    email.send()

@receiver(models.signals.post_save, sender=get_user_model())
def schedule_reminders(sender, instance, created, using, update_fields, **kwargs):
    if sender != get_user_model():
        return
    for reminder in getattr(settings,'REMINDERS',()):
        send_reminder.apply_async((instance, reminder), eta=reminder['ETA'])
