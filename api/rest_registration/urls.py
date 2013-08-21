from rest_framework import routers
from .views import RegistrationView

router = routers.SimpleRouter()
router.register(r'', RegistrationView, 'registration')

urlpatterns = router.urls
