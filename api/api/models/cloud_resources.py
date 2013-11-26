from __future__ import unicode_literals
from logging import getLogger
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from .. import providers
logger = getLogger(__name__)


class Provider(models.Model):
    """Represent a Cloud Compute provider."""
    name = models.CharField("Name", max_length=255)
    code = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    quickstart = models.ForeignKey('Flavor', related_name='+', on_delete=models.PROTECT, null=True)
    launch_time = models.PositiveIntegerField('Time to launch (s)', default=300)

    class Meta:
        app_label = "api"

    @models.permalink
    def get_absolute_url(self):
        return 'provider-detail', [self.pk]

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.quickstart.provider != self:
            raise ValidationError('Provider quickstart flavor must belong to this provider.')


class Region(models.Model):
    """Represent a region in a Cloud"""
    provider = models.ForeignKey(Provider, related_name='regions')
    code = models.CharField("Code", max_length=20)
    name = models.CharField("Name", max_length=255)
    image = models.CharField("Image", max_length=255)
    lbr_region = models.CharField("LBR Region", max_length=20)
    key_name = models.CharField("SSH Key", max_length=255, blank=True)
    security_group = models.CharField("Security Group", max_length=255, blank=True)
    longitude = models.FloatField("Longitude", validators=[MaxValueValidator(180), MinValueValidator(-180)])
    latitude = models.FloatField("Latitude", validators=[MaxValueValidator(90), MinValueValidator(-90)])

    class Meta:
        app_label = "api"

    @models.permalink
    def get_absolute_url(self):
        return 'region-detail', [self.pk]

    def __unicode__(self):
        return self.name

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            self._connection = getattr(providers, self.provider.code)(self)
        return self._connection

    def __getstate__(self):
        if hasattr(self, '_connection'):
            odict = self.__dict__.copy()
            del odict['_connection']
            return odict
        else:
            return self.__dict__


class Flavor(models.Model):
    """Represent a size/type of instance that can be created in a cloud"""
    provider = models.ForeignKey(Provider, related_name='flavors')
    code = models.CharField("Code", max_length=20)
    name = models.CharField("Name", max_length=255)
    description = models.CharField("description", max_length=255, default="", blank=True)
    ram = models.PositiveIntegerField("RAM (MiB)")
    cpus = models.PositiveSmallIntegerField("CPUs")

    class Meta:
        app_label = "api"

    @models.permalink
    def get_absolute_url(self):
        return 'flavor-detail', [self.pk]

    def __unicode__(self):
        return self.name

    @property
    def free_allowed(self):
        return self.provider.quickstart == self
