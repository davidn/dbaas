from rest_framework import routers
from .views import RegistrationView

class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self, trailing_slash=True):
        routers.SimpleRouter.__init__(self, trailing_slash=trailing_slash)
        if trailing_slash=='optional':
            self.trailing_slash='/?'


router = OptionalSlashRouter(trailing_slash='optional')
router.register(r'', RegistrationView, 'registration')

urlpatterns = router.urls
