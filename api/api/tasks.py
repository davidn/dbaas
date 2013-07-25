#!/usr/bin/python

from logging import getLogger
from celery.task import task
from celery import group
from time import sleep
from .models import Node

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

def install_cluster(cluster):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    regions = cluster.regions.filter(launched=False)
    task = wait_nodes.s(install_nodes) | group([install.s(node) for node in install_nodes]) | group([install_region.s(region) for region in regions])
    return task.delay()
