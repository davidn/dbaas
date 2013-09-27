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


def ordinal(num):
    if 4 <= num <= 20 or 24 <= num <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][num % 10 - 1]


@task()
def launch_email(cluster, sendGeneralNotification=True):
    nodes = cluster.nodes.all()
    ctx_dict = {
        'nodes': nodes,
        'username': str(cluster.user),
        'cluster_dns': cluster.dns_name,
        'trial_end': datetime.date.today() + settings.TRIAL_LENGTH,
        'ord': ordinal((datetime.date.today() + settings.TRIAL_LENGTH).day),
        'port': cluster.port,
        'db': cluster.dbname,
        'dbusername': cluster.dbusername,
        'dbpassword': cluster.dbpassword,
        'regions': ' and '.join(node.region.name for node in nodes)
    }

    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string

    subject = render_to_string('confirmation_email_subject.txt', ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message_text = render_to_string('confirmation_email.txt', ctx_dict)
    message_html = render_to_string('confirmation_email.html', ctx_dict)

    recipient = [cluster.user.email] if not sendGeneralNotification else config_value('api_email', 'RECIPIENTS')

    msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, recipient)
    msg.attach_alternative(message_html, "text/html")
    msg.send()


@task()
def launch_cluster(cluster):
    cluster.launch()


def install_cluster(cluster, sendGeneralNotification=True):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = launch_cluster.si(cluster) \
           | wait_nodes.si([node for node in install_nodes]) \
           | group([install.si(node) for node in install_nodes]) \
           | group([install_region.si(lbr_region) for lbr_region in lbr_regions]) \
           | launch_email.si(cluster, sendGeneralNotification)
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
    for reminder in getattr(settings, 'REMINDERS', ()):
        send_reminder.apply_async((instance, reminder), eta=reminder['ETA'])
