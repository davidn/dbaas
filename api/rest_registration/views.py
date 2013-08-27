# Create your views here.
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from registration import signals
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import RegistrationProfile
from .serializers import RegistrationSerializer

class RegistrationView(GenericViewSet):
    permission_classes= (permissions.AllowAny,)
    serializer_class = RegistrationSerializer
    def create(self, request, *args, **kwargs):
        if not self.registration_allowed(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            self.register(request, request.DATA)
            return Response(status=status.HTTP_201_CREATED)
        except:
            raise
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        activated_user = RegistrationProfile.objects.activate_user(kwargs["pk"])
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
            return Response(status.HTTP_202_ACCEPTED, headers={"Location":activated_user.get_absolute_url()})
        return Response(status=status.HTTP_404_NOT_FOUND)

    def register(self, request, data):
        """
        Given an email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, password = data['email'], data['password']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(email,
                                                                    password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)