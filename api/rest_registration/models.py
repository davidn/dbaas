import datetime
import random
import hashlib
from django.utils import timezone
from django.conf import settings
from registration.models import User, RegistrationProfile as BaseRegistrationProfile, RegistrationManager as BaseRegistrationManager
from django.db import transaction, models
from django.utils.translation import ugettext as _
try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now


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

    def forgot_password(self, email, site, send_email=True):
        """
        Validate email address, then regenerate the
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the existing ``User``.

        """
        existing_user = User.objects.get_by_natural_key(email)

        #TODO: If requesting reactivation again, resend the existing activation code. or generate a new one.
        #Currently this errors out.
        registration_profile = self.create_profile(existing_user)

        if send_email:
            registration_profile.send_reactivation_email(site)

        return existing_user

    forgot_password = transaction.commit_on_success(forgot_password)

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

    created_on = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def send_activation_email(self, site, template='registration/activation_email'):
        """Send the activation mail"""

        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'url': settings.FRONTEND_URL}

        self.user.email_user_template(template, ctx_dict)

    def send_reactivation_email(self, site):
        """Send the reactivation mail"""

        self.send_activation_email(site, 'registration/reactivation_email')

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.created_on + expiration_date <= datetime_now())