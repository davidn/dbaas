from time import sleep
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework import viewsets, mixins, status, permissions
from .models import Cluster, Node, Region, Provider, Flavor
from .serializers import UserSerializer, ClusterSerializer, NodeSerializer, RegionSerializer, ProviderSerializer, FlavorSerializer, BackupWriteSerializer, BackupReadSerializer
from .tasks import install, install_cluster
from rest_framework.response import Response
from rest_framework.decorators import action, link, api_view, permission_classes
from django.http.response import HttpResponse
from pyzabbix import ZabbixAPI

class Owner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if isinstance(obj, Cluster):
			return obj.user == request.user
		if isinstance(obj, Node):
			return obj.cluster.user == request.user
		return False
	
	def has_permission(self, request, view):
		return not request.user.is_anonymous()

class IsOwnerOrAdminUserOrCreateMethod(permissions.IsAdminUser):
	def has_object_permission(self, request, view, obj):
		if obj == request.user:
			return True
		return super(IsOwnerOrAdminUserOrCreateMethod, self).has_object_permission(request,view,obj)

	def has_permission(self, request, view):
		if getattr(view, request.method.lower()) == view.create and settings.ALLOW_REGISTRATIONS:
			return True
		return super(IsOwnerOrAdminUserOrCreateMethod, self).has_permission(request, view)

class ProviderViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			viewsets.GenericViewSet):
	serializer_class = ProviderSerializer
	queryset = Provider.objects.filter(enabled=True)
	permission_classes = (permissions.IsAuthenticated,)

class RegionViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			viewsets.GenericViewSet):
	serializer_class = RegionSerializer
	queryset = Region.objects.all()
	permission_classes = (permissions.IsAuthenticated,)

class FlavorViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			viewsets.GenericViewSet):
	serializer_class = FlavorSerializer
	queryset = Flavor.objects.all()
	permission_classes = (permissions.IsAuthenticated,)

class UserViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.CreateModelMixin,
			mixins.UpdateModelMixin,
			viewsets.GenericViewSet):
	model = User
	serializer_class = UserSerializer
	permission_classes = (IsOwnerOrAdminUserOrCreateMethod,)

	def get_queryset(self):
		if self.request.user and self.request.user.is_staff:
			return User.objects.all()
		return User.objects.filter(pk=self.request.user.pk)

@api_view(('GET',))
@permission_classes((permissions.IsAuthenticated,))
def identity(request):
	if not request.user:
		return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
	serializer = UserSerializer(request.user)
	return Response(serializer.data)

class ClusterViewSet(mixins.CreateModelMixin,
			mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.DestroyModelMixin,
			viewsets.GenericViewSet):
	model = Cluster
	serializer_class = ClusterSerializer
	permission_classes = (Owner,)

	def get_queryset(self):
		return Cluster.objects.filter(user=self.request.user)

	def create(self, request, *args, **kwargs):
		if isinstance(request.DATA,list):
			data = []
			for d in request.DATA:
				new_d = d.copy()
				new_d["user"] = reverse('user-detail',args=(request.user.pk,))
				data.append(new_d)
		else:
			data = request.DATA.copy()
			data["user"] = reverse('user-detail',args=(request.user.pk,))
		
		serializer = self.get_serializer(data=data, files=request.FILES)

		if serializer.is_valid():
			self.pre_save(serializer.object)
			self.object = serializer.save(force_insert=True)
			self.post_save(self.object, created=True)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def add(self, request, *args, **kwargs):
		self.object = self.get_object()
		if isinstance(request.DATA,list):
			data = []
			for d in request.DATA:
				new_d = d.copy()
				new_d["cluster"] = self.object.get_absolute_url()
				data.append(new_d)
		else:
			data = request.DATA.copy()
			data["cluster"] = self.object.get_absolute_url()
		serializer = NodeSerializer(data=data, files=request.FILES, context={
			'request': self.request,
			'format': self.format_kwarg,
			'view': self
		})
		if serializer.is_valid():
			if isinstance(serializer.object, list):
				for obj in serializer.object:
					obj.lbr_region = self.object.get_lbr_region_set(obj.region)
			else:
				serializer.object.lbr_region = self.object.get_lbr_region_set(serializer.object.region)
			serializer.save(force_insert=True)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def add_database(self, request, *args, **kwargs):
		self.object = self.get_object()
		for node in self.object.nodes.filter(status=Node.RUNNING):
			node.add_database(request.DATA['dbname'])
		return Response(status=status.HTTP_200_OK)

	@action()
	def launch_all(self, request, *args, **kwargs):
		self.object = self.get_object()
		for node in self.object.nodes.all():
			if node.status == Node.INITIAL:
				node.do_launch()
		install_cluster(self.object)
		serializer = self.get_serializer(self.object)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

def random_walk(initial_value=0, min_value=0, max_value=100, step=2):
	import random
	while True:
		yield initial_value
		initial_value = random.choice((max(min_value, initial_value-step),min(max_value, initial_value+step)))

class NodeViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.DestroyModelMixin,
			viewsets.GenericViewSet):
	model = Node
	serializer_class = NodeSerializer
	permission_classes = (Owner,)

	def get_success_headers(self, data):
		try:
			return {'Location': data['url']}
		except (TypeError, KeyError):
			return {}

	def get_queryset(self):
		return Node.objects.filter(cluster=self.kwargs["cluster"])

	@link(permission_classes=[permissions.AllowAny])
	def cloud_config(self, request, *args, **kwargs):
		self.object = self.get_object()
		for node in self.object.cluster.nodes.filter(status=Node.PROVISIONING):
			while node.pending():
				sleep(15)
		return HttpResponse(self.object.cloud_config, content_type='text/cloud-config')

	def zabbix_history(self, node, key, count=120):
		if node.region.provider.code == 'test':
			from itertools import islice
			return Response(data=list(islice(random_walk(),120)), headers={"X-Data-Source", "test"}, status=status.HTTP_200_OK)
		z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
		z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
		items = z.item.get(host=node.dns_name,filter={"key_":key})
		if len(items) == 0:
			history = []
		else:
			history = [
				float(h['value']) for h in
				z.history.get(itemids=items[0]['itemid'],limit=count,output="extend",history=0)
			]
		return Response(data=history, status=status.HTTP_200_OK)

	@link()
	def cpu(self, request, *args, **kwargs):
		self.object = self.get_object()
		return self.zabbix_history(self.object,"system.cpu.util[]")

	@link()
	def wiops(self, request, *args, **kwargs):
		self.object = self.get_object()
		return self.zabbix_history(self.object,"vfs.dev.write[,ops,]")

	@link()
	def riops(self, request, *args, **kwargs):
		self.object = self.get_object()
		return self.zabbix_history(self.object,"vfs.dev.read[,ops,]")

	@link()
	def stats(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.region.provider.code == 'test':
			from itertools import islice
			return Response(data={
					"cpu":list(islice(random_walk(),120)),
					"wiops":list(islice(random_walk(),120)),
					"riops":list(islice(random_walk(),120))},
				headers={"X-Data-Source", "test"}, status=status.HTTP_200_OK)
		z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
		z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
		res = {}
		for key, key_name in (("system.cpu.util[]","cpu"),("vfs.dev.write[,ops,]","wiops"),("vfs.dev.read[,ops,]","riops")):
			items = z.item.get(host=self.object.dns_name,filter={"key_":key})
			if len(items) != 0:
				res[key_name] = [
					float(h['value']) for h in
					z.history.get(itemids=items[0]['itemid'],limit=120,output="extend",history=0)
				]
		return Response(data=res, status=status.HTTP_200_OK)

	@link()
	def backups(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = BackupReadSerializer(self.object.backups.all())
		return Response(serializer.data)

	@action(permission_classes=[permissions.AllowAny])
	def set_backups(self, request, *args, **kwargs):
		self.object = self.get_object() # The NODE object
		if isinstance(request.DATA,list):
			data = []
			for d in request.DATA:
				new_d = d.copy()
				new_d["node"] = self.object.pk
				data.append(new_d)
		else:
			data = request.DATA.copy()
			data["node"] = self.object.pk
		serializer = BackupWriteSerializer(data=data, files=request.FILES, context={
			'request': self.request,
			'format': self.format_kwarg,
			'view': self
		})
		if serializer.is_valid():
			self.object.backups.all().delete()
			serializer.save(force_insert=True)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def pause(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.pause()
		serializer = self.get_serializer(self.object)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

	@action()
	def resume(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.resume()
		serializer = self.get_serializer(self.object)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
