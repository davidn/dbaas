from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from json import loads
from rest_registration.models import RegistrationProfile
from registration import signals


@require_POST
@csrf_exempt
def register(request):
    try:
        j = loads(request.REQUEST['data.json'])
    except ValueError:
        return HttpResponse(status=400)
    try:
        email = j['email'][0]
    except (TypeError, IndexError, KeyError):
        return HttpResponse(status=400)
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    new_user = RegistrationProfile.objects.create_inactive_user(email, None, site,
                                                                getattr(settings, 'SEND_REGISTRATION_EMAIL', True))
    signals.user_registered.send(sender='unbounce_hook.register',
                                 user=new_user,
                                 request=request)
    return HttpResponse(status=202)
