#!/usr/bin/python

from celery.task import task
from time import sleep
from .models import Node

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
    try:
        node.do_install()
    except:
        node.status = node.ERROR
        node.save()
        raise

@task()
def install_cluster(cluster):
    install_nodes = cluster.node_set.filter(status=Node.PROVISIONING)
    for node in install_nodes:
        while node.pending():
            sleep (15)
    for node in install_nodes:
        install.delay(node)