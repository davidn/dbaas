#!/usr/bin/python
'''
Created on 9 Oct 2013

@author: david
'''

from __future__ import unicode_literals
from celery import group
from .models import Node
from . import tasks

# Controller functions named <VERB>_<OBJECT>

def launch_cluster(cluster):
    cluster.launch_sync()
    for node in cluster.nodes.filter(status=Node.INITIAL):
        node.launch_sync()
    install_nodes = cluster.nodes.filter(status=Node.STARTING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = tasks.cluster_launch_s3.si(cluster) \
         | group([tasks.node_launch_provision.si(node) for node in install_nodes]) \
         | tasks.null_task.si() \
         | group([tasks.node_launch_update.si(node) for node in install_nodes]) \
         | tasks.null_task.si() \
         | group([tasks.node_launch_dns.si(node) for node in install_nodes]) \
         | tasks.cluster_launch_zabbix.si(cluster) \
         | group([tasks.node_launch_zabbix.si(node) for node in install_nodes] \
                +[tasks.region_launch.si(lbr_region) for lbr_region in lbr_regions]) \
         | tasks.wait_zabbix_cluster.si(cluster) \
         | group([tasks.node_launch_complete.si(node) for node in install_nodes]) \
         | tasks.launch_email.si(cluster, 'confirmation_email') \
         | tasks.cluster_launch_complete.si(cluster)
    return task.delay()

def reinstantiate_node(node, flavor):
    if node.reinstantiate_sync(flavor):
        task = tasks.node_reinstantiate.si(node) \
             | tasks.node_reinstantiate_update.si(node) \
             | tasks.node_reinstantiate_complete.si(node) \
             | tasks.wait_zabbix_node.si(node) \
             | tasks.launch_email.si(node.cluster, 'resize_confirmation_email')
        return task.delay()

def pause_node(node):
    node.pause_sync()
    task = tasks.node_pause.si(node) \
         | tasks.node_pause_complete.si(node)
    return task.delay()

def resume_node(node):
    node.resume_sync()
    task = tasks.node_resume_provider.si(node) \
         | tasks.node_resume_dns.si(node) \
         | tasks.node_resume_complete.si(node)
    return task.delay()

def add_database(cluster, dbname):
    cluster.dbname += ','+dbname
    for node in cluster.nodes.filter(status=Node.RUNNING):
        node.add_database(dbname)
    cluster.save()
