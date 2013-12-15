from __future__ import unicode_literals
from logging import getLogger

from django.db import models
import paypalrestsdk
from paypalrestsdk import CreditCard

from dbaas_api import settings

from .uuid_field import UUIDField
from .cloud_resources import Region, Flavor


logger = getLogger(__name__)

# paypalrestsdk.configure({
#     "mode": settings.PAYPAL_MODE,
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_CLIENT_SECRET})

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM",
    "client_secret": "EO422dn3gQLgDbuwqTjzrFgFtaRLRR5BdHEESmha49TM"})


class Pricing(models.Model):
    """Pricing info for Provider, Region, Instance

    """
    uuid = UUIDField(primary_key=True)
    region = models.ForeignKey(Region, related_name='pricing')
    flavor = models.ForeignKey(Flavor, related_name='pricing')
    cost = models.DecimalField('Dollars per server hour', max_digits=8, decimal_places=4)

    class Meta:
        unique_together = (("region", "flavor"),)
        app_label = "api"

    def __repr__(self):
        return "Pricing(region={region}, flavor={flavor})".format(region=repr(self.region), flavor=repr(self.flavor))


class CreditCardTokenManager(models.Manager):
    def create_credit_card(self, cc, user):
        credit_card = CreditCard(cc)

        if credit_card.create():
            logger.error(cc)
            logger.error(credit_card)
            valid_until = credit_card.valid_until[:-10]
            token = self.model(token=credit_card.id, valid_until=valid_until, type=credit_card.type, last4=credit_card.number[-4:],
                               expire_month=credit_card.expire_month, expire_year=credit_card.expire_year, user=user)
            token.save()
            token.user.is_paid = True
            token.user.save()
            return token


class CreditCardToken(models.Model):
    """Result of storing credit card details with Paypal - no PCI information

    """
    id = UUIDField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creditcards')
    token = models.CharField(max_length=40, blank=True, default="")
    valid_until = models.DateField()
    type = models.CharField(max_length=10, blank=True, default="")
    last4 = models.CharField(max_length=4, blank=True, default="")
    expire_month = models.PositiveIntegerField()
    expire_year = models.PositiveIntegerField()

    created_on = models.DateTimeField(auto_now_add=True)

    objects = CreditCardTokenManager()

    class Meta:
        app_label = "api"

    def __unicode__(self):
        return "CreditCardToken(%s %s xxx-%s)" % (self.token, self.type, self.last4)


class Activity(models.Model):
    """ Activity Log

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity')

    action = models.CharField(max_length=50, blank=True, default="")
    detail = models.CharField(max_length=255, blank=True, default="")
    created_on = models.DateTimeField()
    ip = models.CharField(max_length=15, blank=True, default="")
