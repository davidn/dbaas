'''
Created on 9 Oct 2013

@author: david
'''

from celery import group
from .models import Node
from .tasks import install_node, install_region, wait_nodes, wait_nodes_zabbix, launch_email, complete_pause_node, complete_resume_node

def launch_cluster(cluster):
    for node in cluster.nodes.all():
        if node.status == Node.INITIAL:
            node.do_launch()
    install_nodes = cluster.nodes.filter(status=Node.PROVISIONING)
    lbr_regions = cluster.lbr_regions.filter(launched=False)
    task = launch_cluster.si(cluster) \
           | wait_nodes.si([node for node in install_nodes]) \
           | group([install_node.si(node) for node in install_nodes]) \
           | group([install_region.si(lbr_region) for lbr_region in lbr_regions]) \
           | wait_nodes_zabbix.si(cluster) \
           | launch_email.si(cluster)
    return task.delay()

def pause_node(node):
    node.pause()
    complete_pause_node.delay(node)

def resume_node(node):
    node.resume()
    complete_resume_node.delay(node)

def add_database(cluster, dbname):
    cluster.dbname += ','+dbname
    for node in cluster.nodes.filter(status=Node.RUNNING):
        node.add_database(dbname)
    cluster.save()
