#!/usr/bin/python

"""Manage clusters of GenieDB nodes.

This module provides classes to create, manage and destroy clusters of GenieDB
nodes.  It consists of three related classes, Cluster, Node and
LBRRegionNodeSet. Each Cluster contains several Nodes; each cluster has
LBRRegionNodeSet which in turn contain Nodes, such that the LBRRegionNodeSets
partition the Nodes in a cluster. See `the wiki`_ for more info.

.. _the wiki: https://geniedb.atlassian.net/wiki/x/NgCYAQ

"""

from __future__ import unicode_literals
from django.db import models
from django.dispatch.dispatcher import receiver

from .user import User
from .cloud_resources import Provider, Region, Flavor
from .dbaas_resources import Cluster, LBRRegionNodeSet, Node, Backup, BUCKET_NAME
from .rules import Rule
from .pricing import Pricing, CreditCardToken, Activity

@receiver(models.signals.pre_save, sender=Node)
def node_pre_save_callback(sender, instance, raw, using, **kwargs):
    if sender != Node:
        return
    if raw:
        return
    instance.lbr_region = instance.cluster.get_lbr_region_set(instance.region)

@receiver(models.signals.pre_delete, sender=Node)
def node_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Node:
        return
    assert(instance.status in (Node.INITIAL, Node.OVER))


@receiver(models.signals.pre_delete, sender=LBRRegionNodeSet)
def region_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != LBRRegionNodeSet:
        return
    assert(instance.launched is False)


@receiver(models.signals.pre_delete, sender=Cluster)
def cluster_pre_delete_callback(sender, instance, using, **kwargs):
    if sender != Cluster:
        return
    assert(instance.status in (Cluster.INITIAL, Cluster.OVER))
