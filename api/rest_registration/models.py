import random
import hashlib
from django.conf import settings
from registration.models import User, RegistrationProfile as BaseRegistrationProfile, RegistrationManager as BaseRegistrationManager
from django.db import transaction


class RegistrationManager(BaseRegistrationManager):
    def create_inactive_user(self, email, password, site, send_email=True):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.

        """
        new_user = User.objects.create_user(email, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user

    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.

        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.

        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.email
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt + username).hexdigest()
        return self.create(user=user, activation_key=activation_key)


class RegistrationProfile(BaseRegistrationProfile):
    objects = RegistrationManager()

    class Meta:
        proxy = True

    def send_activation_email(self, site, profile):
        """Send the activation mail"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string

        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'email': profile.user.email}

        subject = render_to_string('registration/activation_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string('registration/activation_email.txt', ctx_dict)
        message_html = render_to_string('registration/activation_email.html', ctx_dict)

        msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [self.user.email])
        msg.attach_alternative(message_html, "text/html")
        msg.send()