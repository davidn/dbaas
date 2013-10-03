from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Cluster, Node, Flavor, Provider, Region, Backup
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password
import math
from django.core.exceptions import ValidationError
from api.models import cron_validator
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
    def to_native(self,value):
        return dict(self.choices)[value]

class PasswordField(serializers.CharField):
    def to_native(self, value):
        return None

    def from_native(self, value):
        return make_password(value)

class RamField(serializers.IntegerField):
    def to_native(self, ram_mb_exact):
        # 1. Round base-2 logarithm... ie nearest power of two.
        # 2. Subtract 10 to convert MiB->GiB
        # 3. max(0, ...) to ensure 1GiB minimum
        # 4. 2** to convert back from logarithm to bytes
        ram_gb_approx = 2**max(0,int(round(math.log(ram_mb_exact,2)))-10)
        return serializers.IntegerField.to_native(self, ram_gb_approx)

    def from_native(self, ram_gb):
        # Unwise to use this field in writable serializer as the serialize
        # then deserialize round trip loses data.
        return serializers.IntegerField.from_native(self, ram_gb*1024)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = PasswordField()
    class Meta:
        model = get_user_model()
        fields = ('url','email', 'first_name', 'last_name', 'password', 'is_paid')

    def validate_email(self, attrs, source):
        if self.object is not None and attrs[source] != self.object.email:
            serializers.ValidationError("Email changing disabled")
        return attrs


class FlavorSerializer(serializers.HyperlinkedModelSerializer):
    ram = RamField()
    class Meta:
        model = Flavor
        fields = ('url','code','name','ram','cpus')

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('url','provider', 'code', 'name', 'longitude', 'latitude')

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    flavors = FlavorSerializer(many=True)
    regions = RegionSerializer(many=True)
    class Meta:
        model = Provider
        fields = ('url','name', 'code', 'flavors', 'regions')

class NodeSerializer(serializers.HyperlinkedModelSerializer):
    status = StatusField(choices=Node.STATUSES, read_only=True)
    status_code = serializers.ChoiceField(choices=Node.STATUSES, source='status', read_only=True)
    dns_name = serializers.CharField(read_only=True)
    region = serializers.SlugRelatedField(slug_field='code')
    flavor = serializers.SlugRelatedField(slug_field='code')
    def __init__(self, *args, **kwargs):
        serializers.HyperlinkedModelSerializer.__init__(self, *args, **kwargs)
        url_field = MultiHyperlinkedIdentityField(view_name='node-detail', lookup_field='pk')
        url_field.initialize(self, 'url')
        self.fields['url'] = url_field
    class Meta:
        model = Node
        fields = ('url','label','nid','dns_name','ip','flavor', 'storage', 'region', 'status', 'status_code', 'cluster', 'iops')
        read_only_fields = ('ip','nid')

# This class allows submission as a plain integer (hours)
class CronField(serializers.CharField):
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

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    dns_name = serializers.CharField(read_only=True)
    backup_schedule = CronField()
    class Meta:
        model = Cluster
        fields = ('url','label','user','dbname','dbusername','dbpassword','dns_name','port','nodes', 'backup_count', 'backup_schedule', 'ca_cert', 'client_cert', 'client_key')
        read_only_fields = ('ca_cert', 'client_cert', 'client_key')

class DateUtilField(serializers.DateTimeField):
    def from_native(self, value):
        return serializers.DateTimeField.from_native(self, dateutil.parser.parse(value))

# Serializer for getting data from node
class BackupWriteSerializer(serializers.ModelSerializer):
    time = DateUtilField()
    class Meta:
        model = Backup
        fields = ('node','filename','time','size')

# Serializer for sending data to users
class BackupReadSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_url')
    class Meta:
        model = Backup
        fields = ('url','time','size')
