from time import sleep
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import viewsets, mixins, status, permissions
from .models import Cluster, Node
from .serializers import UserSerializer, ClusterSerializer, NodeSerializer
from .tasks import install, install_cluster
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.http.response import HttpResponse

class Owner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if isinstance(obj, Cluster):
			return obj.user == request.user
		if isinstance(obj, Node):
			return obj.cluster.user == request.user
		return False
	
	def has_permission(self, request, view):
		return not request.user.is_anonymous()

class UserViewSet(mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.CreateModelMixin,
			mixins.UpdateModelMixin,
			viewsets.GenericViewSet):
	serializer_class = UserSerializer
	permission_classes = (Owner,permissions.IsAdminUser)

	def get_queryset(self):
		return User.objects.filter(user=self.request.user)

	@link(permission_classes=[permissions.AllowAny])
	def create(self, *args, **kwargs):
		super(UserViewSet, self).create(*args, **kwargs)

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

	@action()
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
			serializer.save(force_insert=True)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def launch_all(self, request, *args, **kwargs):
		self.object = self.get_object()
		for node in self.object.nodes.all():
			if node.status == Node.INITIAL:
				node.do_launch()
		install_cluster.delay(self.object)
		serializer = self.get_serializer(self.object)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

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

	@action()
	def launch(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.status == Node.INITIAL:
			self.object.do_launch()
			install.delay(self.object)
			serializer = self.get_serializer(self.object)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
