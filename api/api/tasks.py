#!/usr/bin/python

from logging import getLogger
from celery.task import task
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
def install_cluster(cluster):
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    for node in install_nodes:
        while node.pending():
            sleep (15)
    for node in install_nodes:
        install.delay(node)
