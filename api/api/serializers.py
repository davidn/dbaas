from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cluster, Node
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
	password = PasswordField()
	class Meta:
		model = User
		fields = ('url','username', 'first_name', 'last_name', 'email', 'password')

	def validate_username(self, attrs, source):
		if self.object is not None and attrs[source] != self.object.username:
			serializers.ValidationError("Username changing disabled")
		return attrs

class RegionSerializer(serializers.Serializer):
	id = serializers.CharField()
	name = serializers.CharField()

class RegionField(serializers.WritableField):
	def to_native(self, value):
		return value.region

	def from_native(self, value):
		return value

class NodeSerializer(serializers.HyperlinkedModelSerializer):
	status = StatusField(choices=Node.STATUSES, read_only=True)
	dns_name = serializers.CharField(read_only=True)
	region = RegionField(required=True)
	def __init__(self, *args, **kwargs):
		serializers.HyperlinkedModelSerializer.__init__(self, *args, **kwargs)
		url_field = MultiHyperlinkedIdentityField(view_name='node-detail', lookup_field='pk')
		url_field.initialize(self, 'url')
		self.fields['url'] = url_field
	class Meta:
		model = Node
		fields = ('url','instance_id','nid','dns_name','ip','size', 'storage', 'region', 'status', 'cluster', 'iops')
		read_only_fields = ('instance_id','ip','nid')

	def validate_region(self,attrs,source):
		if attrs[source].region not in settings.REGIONS:
			raise serializers.ValidationError("Unsupported Region")
		return attrs

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
	nodes = NodeSerializer(many=True, read_only=True)
	dns_name = serializers.CharField(read_only=True)
	class Meta:
		model = Cluster
		fields = ('url','user','dbname','dbusername','dbpassword','dns_name','port','nodes')
