from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from api import views

admin.autodiscover()

# This class is a customization of the rest_framework router. The only
# difference is the addition of the 'post': 'add' mapping.
class DbaasRouter(routers.SimpleRouter):
    def __init__(self, trailing_slash=True):
        routers.SimpleRouter.__init__(self, trailing_slash=trailing_slash)
        if trailing_slash=='optional':
            self.trailing_slash='/?'

    """Router with added 'add' method to handle POST to an object.
    
    This is needed for our non-standard hierarchical use of the rest_framework.
    
    """
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
router.register(r'clusters/(?P<cluster>[^/]+)', views.NodeViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^register', include('rest_registration.urls')),
    url(r'^api/self', views.identity),
    url(r'^api/cloud_config_by_hostname/(.*)(?:/+)', views.cloud_config_by_hostname),
    url(r'^api/upgrade', views.upgrade),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/?', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
