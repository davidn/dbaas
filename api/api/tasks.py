#!/usr/bin/python

from django.core.mail import send_mail
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
       region = node.region.region,
       node_dns = node.dns_name,
       node_ip = node.ip
    )

def ordinal(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

@task()
def launch_email(cluster):
    nodes = cluster.nodes.all()
    send_mail(
        subject=settings.EMAIL_SUBJECT,
        message=settings.PLAINTEXT_EMAIL_TEMPLATE.format(
            node_text='\n'.join(node_text(node) for node in nodes),
            username=str(cluster.user),
            cluster_dns=cluster.dns_name,
            trial_end=datetime.date.today() + settings.TRIAL_LENGTH,
            ord=ordinal(datetime.date.today() + settings.TRIAL_LENGTH),
            port=node[0].port,
            db='',
            dbusername='',
            dbpassword=''
        ),
        from_email=settings.EMAIL_SENDER,
        recipient_list=settings.EMAIL_RECIPIENTS
    )

def install_cluster(cluster):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    regions = cluster.regions.filter(launched=False)
    task = wait_nodes.si([node for node in install_nodes]) | group([install.si(node) for node in install_nodes]) | group([install_region.si(region) for region in regions]) | launch_email.si(cluster)
    return task.delay()
