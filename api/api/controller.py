#!/usr/bin/python
'''
Created on 9 Oct 2013

@author: david
'''

from __future__ import unicode_literals
import itertools
from celery import group
from .models import Node
from . import tasks


def group_or_null(contents):
    return tasks.null_task.si() if len(contents) == 0 else group(contents)

# Controller functions named <VERB>_<OBJECT>


def launch_cluster(cluster):
    cluster.launch_sync()
    for node in cluster.nodes.filter(status=Node.INITIAL):
        node.launch_sync()
    install_nodes = cluster.nodes.filter(status=Node.STARTING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = tasks.cluster_launch_iam.si(cluster) \
         | group_or_null([tasks.node_launch_provision.si(node) for node in install_nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_update.si(node) for node in install_nodes]).set(countdown=1) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_dns.si(node) for node in install_nodes]) \
         | tasks.cluster_launch_zabbix.si(cluster) \
         | group_or_null([tasks.node_launch_salt.si(node) for node in install_nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_zabbix.si(node) for node in install_nodes]
                +[tasks.region_launch.si(lbr_region) for lbr_region in lbr_regions]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_complete.si(node) for node in install_nodes]) \
         | tasks.launch_email.si(cluster, 'confirmation_email') \
         | tasks.cluster_launch_complete.si(cluster)
    return task.delay()


def shutdown_cluster(cluster):
    cluster.shutdown_sync()
    for node in cluster.nodes.exclude(status=Node.INITIAL):
        node.shutdown_sync()
    shutdown_nodes = cluster.nodes.filter(status=Node.SHUTTING_DOWN)
    lbr_regions = cluster.lbr_regions.filter(launched=True)
    task = group_or_null([tasks.node_shutdown_zabbix.si(node) for node in shutdown_nodes]
                 + [tasks.node_shutdown_dns.si(node) for node in shutdown_nodes]
                 + [tasks.node_shutdown_instance.si(node) for node in shutdown_nodes]) \
        | tasks.null_task.si() \
        | group_or_null([tasks.region_shutdown.si(lbr_region) for lbr_region in lbr_regions]) \
        | tasks.null_task.si() \
        | group_or_null([tasks.node_shutdown_complete.si(node) for node in shutdown_nodes]) \
        | tasks.null_task.si() \
        | group_or_null([tasks.region_shutdown_complete.si(lbr_region) for lbr_region in lbr_regions]) \
        | tasks.cluster_shutdown.si(cluster)
    return task.delay()


def reinstantiate_node(node, flavor):
    if node.reinstantiate_sync(flavor):
        task = tasks.node_reinstantiate_setup.si(node) \
             | tasks.node_reinstantiate_main.si(node) \
             | tasks.node_reinstantiate_update.si(node) \
             | tasks.node_reinstantiate_zabbix.si(node) \
             | tasks.node_reinstantiate_complete.si(node) \
             | tasks.launch_email.si(node.cluster, 'resize_confirmation_email')
        return task.delay()


def pause_node(node):
    node.pause_sync()
    task = tasks.node_pause_salt.si(node) \
         | tasks.node_pause_complete.si(node)
    return task.delay()


def resume_node(node):
    node.resume_sync()
    task = tasks.node_resume_salt.si(node) \
         | tasks.node_resume_complete.si(node)
    return task.delay()


def shutdown_node(node):
    node.shutdown_sync()
    task = tasks.node_shutdown_zabbix.si(node) \
         | tasks.node_shutdown_dns.si(node) \
         | tasks.node_shutdown_instance.si(node) \
         | tasks.cluster_refresh_salt.si(node.cluster) \
         | tasks.node_shutdown_complete.si(node)
    return task.delay()

def add_database(cluster, dbname):
    cluster.add_database_sync(dbname)
    task = tasks.cluster_refresh_salt.si(cluster) \
         | group_or_null([tasks.node_refresh_complete.si(node) for node in cluster.nodes.filter(status=Node.RUNNING)])
    task.delay()


def add_nodes(nodes):
    for node in nodes:
        node.launch_sync()
    cluster = nodes[0].cluster
    task = group_or_null([tasks.node_launch_provision.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_update.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_dns.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_salt.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_zabbix.si(node) for node in nodes]
                +[tasks.region_launch.si(lbr_region) for lbr_region in set(node.lbr_region for node in nodes)]) \
         | tasks.null_task.si() \
         | tasks.cluster_refresh_salt.si(cluster, cluster.nodes.filter(
             status__in=[Node.RUNNING, Node.PAUSING, Node.PAUSED, Node.RESUMING])) \
         | group_or_null([tasks.node_refresh_complete.si(node) for node in cluster.nodes.filter(
             status__in=[Node.RUNNING, Node.PAUSING, Node.PAUSED, Node.RESUMING])]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_add_copy.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_add_copy_complete.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | tasks.cluster_refresh_salt.si(cluster, nodes) \
         | group_or_null([tasks.node_refresh_complete.si(node) for node in nodes]) \
         | tasks.null_task.si() \
         | group_or_null([tasks.node_launch_complete.si(node) for node in nodes]) \
         | tasks.launch_email.si(cluster, 'add_node_confirmation_email')
    return task.delay()
