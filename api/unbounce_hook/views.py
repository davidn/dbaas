from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.sites import Site
from django.conf import settings
from json import loads
from rest_registration.models import RegistrationProfile
from registration import signals


@require_POST
def register(request):
    try:
        j = loads(request.body)
    except ValueError:
        return HttpResponse(status=400)
    try:
        email = j['email_address'][0]
    except TypeError, IndexError, KeyError:
        return HttpResponse(status=400)
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    new_user = RegistrationProfile.objects.create_inactive_user(email, None, site,
                                                                getattr(settings, 'SEND_REGISTRATION_EMAIL', True))
    signals.user_registered.send(sender=self.__class__,
                                 user=new_user,
                                 request=request)
    return HttpResponse(status=202)
