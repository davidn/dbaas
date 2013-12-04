from __future__ import unicode_literals
from logging import getLogger

from django.db import models
import paypalrestsdk
from paypalrestsdk import CreditCard

from dbaas_api import settings

from .uuid_field import UUIDField
from .cloud_resources import Region, Flavor


logger = getLogger(__name__)

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

    class Meta:
        app_label = "api"

    def __unicode__(self):
        return "CreditCardToken(%s %s xxx-)" % (self.token, self.type, self.last4)


class CreditCardTokenManager(models.Manager):
    def create_credit_card(self, params):
        credit_card = CreditCard({
            "type": "visa",
            "number": "4417119669820331",
            "expire_month": "11",
            "expire_year": "2018",
            "cvv2": "874",
            "first_name": "Joe",
            "last_name": "Shopper",
            "billing_address": {
                "line1": "52 N Main ST",
                "city": "Johnstown",
                "state": "OH",
                "postal_code": "43210",
                "country_code": "US"}})

        if credit_card.create():
            token = self.model(token=credit_card.id, valid_until=credit_card.valid_until, type=credit_card.type, last4=credit_card.last4,
                               expire_month=credit_card.expire_month, expire_year=credit_card.expire_year)
            return token


class Activity(models.Model):
    """ Activity Log

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity')

    action = models.CharField(max_length=50, blank=True, default="")
    detail = models.CharField(max_length=255, blank=True, default="")
    created_on = models.DateTimeField()
    ip = models.CharField(max_length=15, blank=True, default="")
