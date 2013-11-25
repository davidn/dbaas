from rest_framework import routers
from .views import RegistrationView

# This class is a customization of the rest_framework router. The only
# difference is 'patch': 'partial_update' operates on the main list.
class ListPatchRouter(routers.SimpleRouter):
    def __init__(self, trailing_slash=True):
        routers.SimpleRouter.__init__(self, trailing_slash=trailing_slash)
        if trailing_slash=='optional':
            self.trailing_slash='/?'

    routes = [
        # List route.
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'patch': 'partial_update'
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
                'delete': 'destroy'
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


router = ListPatchRouter(trailing_slash='optional')
router.register(r'', RegistrationView, 'registration')

urlpatterns = router.urls
