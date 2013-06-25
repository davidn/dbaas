from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status, permissions
from .models import Cluster, Node
from .serializers import UserSerializer, ClusterSerializer, NodeSerializer
from .tasks import install, install_cluster
from rest_framework.response import Response
from rest_framework.decorators import action

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
			viewsets.GenericViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class ClusterViewSet(mixins.CreateModelMixin,
			mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.DestroyModelMixin,
			viewsets.GenericViewSet):
	queryset = Cluster.objects.all()
	serializer_class = ClusterSerializer
	permission_classes = (Owner,)

	def create(self, request, *args, **kwargs):
		if isinstance(request.DATA,list):
			data = []
			for d in request.DATA:
				new_d = d.copy()
				new_d["user"] = request.user.get_absolute_url()
				data.append(new_d)
		else:
			data = request.DATA.copy()
			data["cluster"] = request.user.get_absolute_url()
		
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
			self.object = serializer.save(force_insert=True)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def launch_all(self, request, *args, **kwargs):
		self.object = self.get_object()
		for node in self.object.node_set.all():
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