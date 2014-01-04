from __future__ import unicode_literals
from logging import getLogger
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext as _

logger = getLogger(__name__)
email_logger = getLogger('api.email')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_paid = models.BooleanField(_('paid'), default=False,
                                  help_text=_('Designates whether this user should be allowed to '
                                              'create arbitrary nodes and clusters.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = "api"

    @models.permalink
    def get_absolute_url(self):
        return 'user-detail', [self.pk]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, message_html=None):
        """
        Sends an email to this User.
        """
        from django.core.mail import EmailMultiAlternatives

        recipient = [settings.OVERRIDE_USER_EMAIL] if getattr(settings, 'OVERRIDE_USER_EMAIL', False) else [self.email]

        bcc_recipient = settings.INTERNAL_BCC_EMAIL if getattr(settings, 'INTERNAL_BCC_EMAIL', False) else None

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMultiAlternatives(subject, message, from_email, recipient, bcc=bcc_recipient)
        if message_html:
            msg.attach_alternative(message_html, "text/html")

        try:
            msg.send()
            email_logger.info("Sent email to '%s' from '%s', subject '%s'.", recipient, from_email, subject)
        except:
            email_logger.info("Failed to send email to '%s' from '%s', subject '%s'.", recipient, from_email, subject,
                              exc_info=True)
            raise


    def email_user_template(self, template_base_name, dictionary, *args, **kwargs):
        """
        Sends a multipart html email to this User.
        """
        from django.template.loader import render_to_string

        subject = render_to_string(template_base_name + '_subject.txt', dictionary)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string(template_base_name + '.txt', dictionary)
        message_html = render_to_string(template_base_name + '.html', dictionary)

        self.email_user(subject, message_text, message_html=message_html, *args, **kwargs)
