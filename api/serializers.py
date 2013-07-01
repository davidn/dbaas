from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cluster, Node
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse

class MultiHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
	def get_url(self, obj, view_name, request, format):
		"""
		Given an object, return the URL that hyperlinks to the object.

		May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
		attributes are not configured to correctly match the URL conf.
		"""
		lookup_field = getattr(obj, self.lookup_field)
		kwargs = {self.lookup_field: lookup_field, 'cluster': obj.cluster.id}
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

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('username',)

class NodeSerializer(serializers.HyperlinkedModelSerializer):
	status = StatusField(choices=Node.STATUSES, read_only=True)
	def __init__(self, *args, **kwargs):
		serializers.HyperlinkedModelSerializer.__init__(self, *args, **kwargs)
		url_field = MultiHyperlinkedIdentityField(view_name='node-detail', lookup_field='pk')
		url_field.initialize(self, 'url')
		self.fields['url'] = url_field
	class Meta:
		model = Node
		fields = ('instance_id','dns','ip','size', 'storage', 'region', 'status', 'cluster', 'iops')
		read_only_fields = ('instance_id','dns','ip')

	def validate_region(self,attrs,source):
		if attrs[source] not in settings.EC2_REGIONS:
			raise serializers.ValidationError("Unsupported Region")
		return attrs

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
	nodes = NodeSerializer(many=True, read_only=True)
	class Meta:
		model = Cluster
		fields = ('user','nodes')
