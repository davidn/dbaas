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

class MysqlSetupField(serializers.WritableField):
	def field_from_native(self, data, files, field_name, into):
		"""
		Given a dictionary and a field name, updates the dictionary `into`,
		with the field and it's deserialized value.
		"""
		if self.read_only:
			return

		try:
			if self.use_files:
				files = files or {}
				native = files[field_name]
			else:
				native = data[field_name]
		except KeyError:
			if self.default is not None and not self.partial:
				# Note: partial updates shouldn't set defaults
				if serializers.is_simple_callable(self.default):
					native = self.default()
				else:
					native = self.default
			else:
				databases = data['databases'] if 'databases' in data else []
				username = data['username'] if 'username' in data else 'geniedb'
				password = data['password'] if 'password' in data else 'password'
				native = ''.join('CREATE DATABASE {0};'.format(db) for db in databases) + \
					"CREATE USER '{0}'@'%' IDENTIFIED BY '{1}';".format(username, password) + \
					''.join("GRANT ALL ON {0}.* to '{1}'@'%';".format(db,username) for db in databases) 

		value = self.from_native(native)
		if self.source == '*':
			if value:
				into.update(value)
		else:
			self.validate(value)
			self.run_validators(value)
			into[self.source or field_name] = value

class NodeSerializer(serializers.HyperlinkedModelSerializer):
	status = StatusField(choices=Node.STATUSES, read_only=True)
	mysql_setup = MysqlSetupField()
	def __init__(self, *args, **kwargs):
		serializers.HyperlinkedModelSerializer.__init__(self, *args, **kwargs)
		url_field = MultiHyperlinkedIdentityField(view_name='node-detail', lookup_field='pk')
		url_field.initialize(self, 'url')
		self.fields['url'] = url_field
	class Meta:
		model = Node
		fields = ('instance_id','nid','dns','ip','size', 'storage', 'region', 'status', 'cluster', 'iops', 'mysql_setup')
		read_only_fields = ('instance_id','dns','ip','nid')

	def validate_region(self,attrs,source):
		if attrs[source] not in settings.EC2_REGIONS:
			raise serializers.ValidationError("Unsupported Region")
		return attrs

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
	nodes = NodeSerializer(many=True, read_only=True)
	class Meta:
		model = Cluster
		fields = ('user','nodes')
