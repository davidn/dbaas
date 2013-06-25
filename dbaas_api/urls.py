from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from api import views

admin.autodiscover()

class DbaasRouter(routers.SimpleRouter):
    routes = [
        # List route.
        routers.Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        routers.Route(
            url=r'^{prefix}/{lookup}/$',
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
            url=r'^{prefix}/{lookup}/{methodname}/$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

router = DbaasRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clusters', views.ClusterViewSet)
router.register(r'clusters/(?P<cluster>[^/]+)', views.NodeViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbaas_api.views.home', name='home'),
    # url(r'^dbaas_api/', include('dbaas_api.foo.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
