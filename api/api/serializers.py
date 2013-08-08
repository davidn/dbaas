from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cluster, Node, Flavor, Provider, Region
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password
import math

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
		model = User
		fields = ('url','username', 'first_name', 'last_name', 'email', 'password')

	def validate_username(self, attrs, source):
		if self.object is not None and attrs[source] != self.object.username:
			serializers.ValidationError("Username changing disabled")
		return attrs


class FlavorSerializer(serializers.HyperlinkedModelSerializer):
	ram = RamField()
	class Meta:
		model = Flavor
		fields = ('url','code','name','ram','cpus')

class RegionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Region
		fields = ('url','provider', 'code', 'name')

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
	flavors = FlavorSerializer(many=True)
	regions = RegionSerializer(many=True)
	class Meta:
		model = Provider
		fields = ('url','name', 'code', 'flavors', 'regions')

class NodeSerializer(serializers.HyperlinkedModelSerializer):
	status = StatusField(choices=Node.STATUSES, read_only=True)
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
		fields = ('url','label','nid','dns_name','ip','flavor', 'storage', 'region', 'status', 'cluster', 'iops')
		read_only_fields = ('ip','nid')

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
	nodes = NodeSerializer(many=True, read_only=True)
	dns_name = serializers.CharField(read_only=True)
	class Meta:
		model = Cluster
		fields = ('url','label','user','dbname','dbusername','dbpassword','dns_name','port','nodes')
