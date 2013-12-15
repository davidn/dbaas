#!/usr/bin/python
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views


class DbaasRouter(routers.SimpleRouter):
    """Router with added 'add' method to handle POST to an object.

    This is needed for our non-standard hierarchical use of the rest_framework.

    """
    def __init__(self, trailing_slash=True):
        routers.SimpleRouter.__init__(self, trailing_slash=trailing_slash)
        if trailing_slash == 'optional':
            self.trailing_slash = '/?'

    routes = [
        # List route.
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        routers.Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
                'post': 'add'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated routes.
        # Generated using @action or @link decorators on methods of the viewset.
        routers.Route(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

router = DbaasRouter(trailing_slash='optional')
router.register(r'users', views.UserViewSet)
router.register(r'clusters', views.ClusterViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'flavor', views.FlavorViewSet)
router.register(r'cc', views.CreditCardViewSet)
router.register(r'clusters/(?P<cluster>[^/]+)', views.NodeViewSet)
router.register(r'clusters/(?P<cluster>[^/]+)/(?P<node>[^/]+)/backups', views.BackupViewSet)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
                       url(r'self', views.identity),
                       url(r'upgrade', views.upgrade))
