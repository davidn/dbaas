#!/usr/bin/python

"""An API providing users access to the facilities provided by :py:mod:`~api.models`.

There are several aspects to the API, each with their own class (a viewset):

* Listing :py:class:`~api.models.Provider`, :py:class:`~api.models.Region` and :py:class:`~api.models.Flavor`

* Listing :py:class:`User`

* Listing, creating, launching and deleting :py:class:`~api.models.Cluster`.

* Listing, creating, pausing, resuming, viewing stats of, viewing backups of and deleting :py:class:`~api.models.Node`.

"""

from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins
from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins, status, permissions
from .models import Cluster, Node, Region, Provider, Flavor, Backup
from .serializers import UserSerializer, ClusterSerializer, NodeSerializer, RegionSerializer, ProviderSerializer, FlavorSerializer, BackupWriteSerializer, BackupReadSerializer
from .controller import launch_cluster, reinstantiate_node, pause_node, resume_node, add_database, add_nodes
from rest_framework.response import Response
from rest_framework.decorators import action, link, api_view, permission_classes
from django.http.response import HttpResponse
from pyzabbix import ZabbixAPI
from api.utils import mysql_database_validator


class Owner(permissions.BasePermission):
    """Allows a user access to Clusters and Nodes she owns."""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Cluster):
            return obj.user == request.user
        if isinstance(obj, Node):
            return obj.cluster.user == request.user
        if isinstance(obj, Backup):
            return obj.node.cluster.user == request.user
        return False

    def has_permission(self, request, view):
        return not request.user.is_anonymous()


class IsOwnerOrAdminUser(permissions.IsAdminUser):
    """Allows owners or admins access, and allows anyone create access."""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return super(IsOwnerOrAdminUser, self).has_object_permission(request, view, obj)


class ProviderViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """List and retrieve :py:class:`~api.Provider`."""
    serializer_class = ProviderSerializer
    queryset = Provider.objects.filter(enabled=True)
    permission_classes = (permissions.IsAuthenticated,)


class RegionViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """List and retrieve :py:class:`~api.Region`."""
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class FlavorViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """List and retrieve :py:class:`~api.Flavor`."""
    serializer_class = FlavorSerializer
    queryset = Flavor.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """List, retrieve update and create :py:class:`~api.Region`."""
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return get_user_model().objects.all()
        return get_user_model().objects.filter(pk=self.request.user.pk)


@api_view(('GET',))
@permission_classes((permissions.IsAuthenticated,))
def identity(request):
    """Tell the logged in user about herself."""
    if not request.user:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(('POST',))
@permission_classes((permissions.IsAuthenticated,))
def upgrade(request):
    if not request.user:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    mail_admins("User wants to upgrade", "User %s wants to upgrade" % request.user)
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

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
        if isinstance(request.DATA, list):
            data = []
            n = len(request.DATA)
            for d in request.DATA:
                new_d = d.copy()
                new_d["user"] = reverse('user-detail', args=(request.user.pk,))
                data.append(new_d)
        else:
            data = request.DATA.copy()
            data["user"] = reverse('user-detail', args=(request.user.pk,))
            n = 1

        if not request.user.is_paid and request.user.clusters.count() + n > 1:
            return Response({'non_field_errors': ['Free users cannot create more than one cluster']}, status=status.HTTP_403_FORBIDDEN)

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
        if isinstance(request.DATA, list):
            data = []
            n = len(request.DATA)
            for d in request.DATA:
                new_d = d.copy()
                new_d["cluster"] = self.object.get_absolute_url()
                data.append(new_d)
        else:
            data = request.DATA.copy()
            data["cluster"] = self.object.get_absolute_url()
            n = 1

        if not request.user.is_paid and self.object.nodes.count() + n > 2:
            return Response({'non_field_errors': ['Free users cannot create more than two nodes']}, status=status.HTTP_403_FORBIDDEN)

        serializer = NodeSerializer(data=data, files=request.FILES, context={
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        })

        if not request.user.is_paid and (
                isinstance(serializer.object, list) and any(not serializer.object.flavor.free_allowed for n in serializer.object)) or (
                isinstance(serializer.object, Node) and not serializer.object.flavor.free_allowed):
            return Response({'non_field_errors': ['Free users cannot create this flavor node']}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save(force_insert=True)
            if self.object.status == Cluster.RUNNING:
                add_nodes(serializer.object if isinstance(serializer.object, list) else [serializer.object])
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action()
    def add_database(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            mysql_database_validator(request.DATA['dbname'])
            add_database(self.object, request.DATA['dbname'])
            serializer = self.get_serializer(self.object)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        except ValidationError, e:
            return Response({'dbname': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    @action()
    def launch(self, request, *args, **kwargs):
        self.object = self.get_object()
        launch_cluster(self.object)
        serializer = self.get_serializer(self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
    launch_all = launch


def random_walk(initial_value=0, min_value=0, max_value=100, step=2):
    import random

    while True:
        yield initial_value
        initial_value = random.choice((max(min_value, initial_value - step), min(max_value, initial_value + step)))


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

    def zabbix_history(self, node, key, count=120):
        if node.region.provider.code == 'test':
            from itertools import islice
            #return Response(data=list(islice(random_walk(),120)), headers={"X-Data-Source", "test"}, status=status.HTTP_200_OK)
            return Response(data=list(islice(random_walk(), 120)), status=status.HTTP_200_OK)
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        items = z.item.get(host=node.dns_name, filter={"key_": key})
        if len(items) == 0:
            history = []
        else:
            history = [
                float(h['value']) for h in
                z.history.get(itemids=items[0]['itemid'], limit=count,
                              output="extend", history=0, sortorder="DESC",
                              sortfield="clock")
            ]
            history.reverse()
        return Response(data=history, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_object = self.get_object()
        serializer = self.get_serializer(new_object, data=request.DATA, partial=True)
        if serializer.is_valid():
            if not new_object.flavor.provider:
                new_object.flavor.provider = self.object.flavor.provider
            elif new_object.flavor.provider != self.object.flavor.provider:
                return Response({'dbname': ["Cannot change provider from %s (attempted to change to %s)" % (self.object.flavor.provider, new_object.flavor.provider)]}, status=status.HTTP_400_BAD_REQUEST)
            if not new_object.flavor.code:
                new_object.flavor.code = self.object.flavor.code
            if not new_object.flavor.name:
                new_object.flavor.name = self.object.flavor.name
            if not new_object.flavor.free_allowed:
                new_object.flavor.free_allowed = self.object.flavor.free_allowed
            elif new_object.flavor.free_allowed != self.object.flavor.free_allowed:
                return Response({'dbname': ["Cannot change free users allowed status from %s (attempted to change to %s)" % (self.object.flavor.free_allowed, new_object.flavor.free_allowed)]}, status=status.HTTP_400_BAD_REQUEST)
            if new_object.flavor.code != self.object.flavor.code:
                reinstantiate_node(self.object, new_object.flavor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @link()
    def cpu(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.zabbix_history(self.object, "system.cpu.util[]")

    @link()
    def wiops(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.zabbix_history(self.object, "vfs.dev.write[,ops,]")

    @link()
    def riops(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.zabbix_history(self.object, "vfs.dev.read[,ops,]")

    @link()
    def stats(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.region.provider.code == 'test':
            from itertools import islice

            return Response(data={
                "cpu": list(islice(random_walk(), 120)),
                "wiops": list(islice(random_walk(), 120)),
                "riops": list(islice(random_walk(), 120))},
                            headers={"X-Data-Source": "test"}, status=status.HTTP_200_OK)
        z = ZabbixAPI(settings.ZABBIX_ENDPOINT)
        z.login(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        res = {}
        for key, key_name in (("system.cpu.util[]", "cpu"), ("vfs.dev.write[,ops,]", "wiops"), ("vfs.dev.read[,ops,]", "riops")):
            items = z.item.get(host=self.object.dns_name, filter={"key_": key})
            if len(items) != 0:
                res[key_name] = [
                    float(h['value']) for h in
                    z.history.get(itemids=items[0]['itemid'], limit=120,
                                  output="extend", history=0, sortorde="DESC",
                                  sortfield="clock")
                ]
                res[key_name].reverse()
        return Response(data=res, status=status.HTTP_200_OK)

    @action()
    def pause(self, request, *args, **kwargs):
        self.object = self.get_object()
        pause_node(self.object)
        serializer = self.get_serializer(self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

    @action()
    def resume(self, request, *args, **kwargs):
        self.object = self.get_object()
        resume_node(self.object)
        serializer = self.get_serializer(self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

class OwnerOrCreate(Owner):
    def has_permission(self, request, view):
        return view.action == 'create' or not request.user.is_anonymous()

class BackupViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    model = Backup
    serializer_class = BackupReadSerializer
    permission_classes = (OwnerOrCreate,)

    def get_queryset(self):
        return Backup.objects.filter(node=self.kwargs["node"])

    def get_success_headers(self, data):
        try:
            return {'Location': data['url']}
        except (TypeError, KeyError):
            return {}

    def create(self, request, *args, **kwargs):
        if isinstance(request.DATA, list):
            data = []
            for d in request.DATA:
                new_d = d.copy()
                new_d['node'] = self.kwargs["node"]
                data.append(new_d)
        else:
            data = request.DATA.copy()
            data['node'] = self.kwargs["node"]
        serializer = BackupWriteSerializer(data=data, files=request.FILES)

        if serializer.is_valid():
            self.get_queryset().delete()
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
