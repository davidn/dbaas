#!/usr/bin/python
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from rest_framework_nested import routers
from api import views


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'users', views.UserViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'flavor', views.FlavorViewSet)
router.register(r'cc', views.CreditCardViewSet)

router.register(r'clusters', views.ClusterViewSet)
clusters_router = routers.NestedSimpleRouter(router, r'clusters', lookup='cluster', trailing_slash=False)

clusters_router.register(r'nodes', views.NodeViewSet)
nodes_router = routers.NestedSimpleRouter(clusters_router, r'nodes', lookup='node', trailing_slash=False)

nodes_router.register(r'backups', views.BackupViewSet)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
                       url(r'', include(clusters_router.urls)),
                       url(r'^clusters/(?P<cluster_pk>[^/]+)/', include(nodes_router.urls)),
                       url(r'self', views.identity),
                       url(r'upgrade', views.upgrade))
