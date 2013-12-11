from django.conf.urls import patterns, url
from .views import register

urlpatterns = patterns('',
                       url('register', register))
