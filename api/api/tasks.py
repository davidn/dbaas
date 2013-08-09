#!/usr/bin/python

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from logging import getLogger
from celery.task import task
from celery import group
from time import sleep
from .models import Node
import datetime

logger = getLogger(__name__)

@task()
def launch(node):
    try:
        node.do_launch()
    except:
        node.status = node.ERROR
        node.save()
        raise

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
    return settings.PLAINTEXT_PER_NODE.format(
       nid = node.nid,
       region = node.region.name,
       node_dns = node.dns_name,
       node_ip = node.ip
    )

def node_html(node):
    return settings.HTML_PER_NODE.format(
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
        subject=settings.EMAIL_SUBJECT,
        body=settings.PLAINTEXT_EMAIL_TEMPLATE.format(**params),
        from_email=settings.EMAIL_SENDER,
        to=settings.EMAIL_RECIPIENTS
    )
    email.attach_alternative(
        settings.HTML_EMAIL_TEMPLATE.format(**params),
        "text/html"
    )
    email.send()

def install_cluster(cluster):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = wait_nodes.si([node for node in install_nodes]) | group([install.si(node) for node in install_nodes]) | group([install_region.si(lbr_region) for lbr_region in lbr_regions]) | launch_email.si(cluster)
    return task.delay()
