#!/usr/bin/python
from __future__ import unicode_literals
import re
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Cluster, Node, Flavor, Provider, Region, Backup, CreditCardToken
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .utils import cron_validator, comma_separated_mysql_database_validator
import dateutil.parser


class MultiHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        lookup_field = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_field: lookup_field, 'cluster': obj.cluster.pk}
        try:
            return reverse(view_name, kwargs=kwargs, request=request, format=format)
        except NoReverseMatch:
            pass

        if self.pk_url_kwarg != 'pk':
            # Only try pk lookup if it has been explicitly set.
            # Otherwise, the default `lookup_field = 'pk'` has us covered.
            kwargs = {self.pk_url_kwarg: obj.pk}
            try:
                return reverse(view_name, kwargs=kwargs, request=request, format=format)
            except NoReverseMatch:
                pass

        slug = getattr(obj, self.slug_field, None)
        if slug:
            # Only use slug lookup if a slug field exists on the model
            kwargs = {self.slug_url_kwarg: slug}
            try:
                return reverse(view_name, kwargs=kwargs, request=request, format=format)
            except NoReverseMatch:
                pass

        raise NoReverseMatch()


class StatusField(serializers.ChoiceField):
    def to_native(self, value):
        return dict(self.choices)[value]


class PasswordField(serializers.CharField):
    def to_native(self, value):
        return None

    def from_native(self, value):
        return make_password(value)


class UserExpiryField(serializers.DateTimeField):
    def to_native(self, user):
        if user.is_paid:
            return ''
        q = Cluster.history.filter(user_id=user.id, status=Cluster.PROVISIONING).order_by('-history_date')
        try:
            first_cluster = q[0]
        except IndexError:
            return ''
        return first_cluster.history_date + settings.TRIAL_LENGTH


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = PasswordField()
    expiry = UserExpiryField(source='*', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'is_paid', 'expiry')
        read_only_fields = ('email', 'is_paid')


class FlavorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flavor
        fields = ('url', 'code', 'name', 'ram', 'cpus', 'description', 'variable_storage_available',
                  'variable_storage_default', 'fixed_storage', 'free_allowed')


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('url', 'provider', 'code', 'name', 'longitude', 'latitude')


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    flavors = FlavorSerializer(many=True)
    regions = RegionSerializer(many=True)

    class Meta:
        model = Provider
        fields = ('url', 'name', 'code', 'flavors', 'regions', 'quickstart', 'launch_time')


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    status = StatusField(choices=Node.STATUSES, read_only=True)
    status_code = serializers.ChoiceField(choices=Node.STATUSES, source='status', read_only=True)
    dns_name = serializers.CharField(read_only=True)
    region = serializers.SlugRelatedField(slug_field='code')
    flavor = serializers.SlugRelatedField(slug_field='code')
    feature_flags = serializers.SerializerMethodField('get_feature_flags')

    def __init__(self, *args, **kwargs):
        serializers.HyperlinkedModelSerializer.__init__(self, *args, **kwargs)
        url_field = MultiHyperlinkedIdentityField(view_name='node-detail', lookup_field='pk')
        url_field.initialize(self, 'url')
        self.fields['url'] = url_field

    class Meta:
        model = Node
        fields = ('url', 'label', 'nid', 'dns_name', 'ip', 'flavor', 'storage', 'region', 'status', 'status_code',
                  'cluster', 'iops')
        read_only_fields = ('ip', 'nid')

    @staticmethod
    def get_feature_flags(obj):
        return obj.feature_flags


class CronField(serializers.CharField):
    """This class allows submission as a plain integer (hours)"""

    def from_native(self, value):
        try:
            cron_validator(value)
            return value
        except ValidationError as e:
            try:
                h = int(value, 10)
            except:
                raise e
            if h < 1:
                raise e
            return "0 */%d * * *" % h


class DatabaseNameField(serializers.CharField):
    def from_native(self, value):
        value = ",".join(set(re.findall(r'[^, ]+', value)))
        comma_separated_mysql_database_validator(value)
        return super(DatabaseNameField, self).from_native(value)


class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    status = StatusField(choices=Cluster.STATUSES, read_only=True)
    status_code = serializers.ChoiceField(choices=Cluster.STATUSES, source='status', read_only=True)
    id = serializers.CharField(source='pk', read_only=True)
    nodes = NodeSerializer(many=True, read_only=True)
    dns_name = serializers.CharField(read_only=True)
    dbname = DatabaseNameField()
    backup_schedule = CronField()
    feature_flags = serializers.SerializerMethodField('get_feature_flags')

    class Meta:
        model = Cluster
        fields = ('url', 'id', 'label', 'status', 'status_code', 'user', 'dbname', 'dbusername', 'dbpassword',
                  'dns_name', 'port', 'nodes', 'backup_count', 'backup_schedule', 'ca_cert', 'client_cert',
                  'client_key')
        read_only_fields = ('ca_cert', 'client_cert', 'client_key')

    @staticmethod
    def get_feature_flags(obj):
        return obj.feature_flags


class DateUtilField(serializers.DateTimeField):
    def from_native(self, value):
        return serializers.DateTimeField.from_native(self, dateutil.parser.parse(value))


class BackupWriteSerializer(serializers.ModelSerializer):
    """Serializer for getting data from node"""
    time = DateUtilField()

    class Meta:
        model = Backup
        fields = ('node', 'filename', 'time', 'size')


class BackupReadSerializer(serializers.ModelSerializer):
    """Serializer for sending data to users"""
    url = serializers.CharField(source='get_url')

    class Meta:
        model = Backup
        fields = ('url', 'time', 'size')


class CreditCardSerializer(serializers.ModelSerializer):
    """Serializer for sending data to users"""

    class Meta:
        model = CreditCardToken
        fields = ('valid_until', 'last4', 'expire_month', 'expire_year')

