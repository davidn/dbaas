from .views import register

urlpatterns = patterns('',
                       url('register', register))
