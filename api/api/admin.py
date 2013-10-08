from .models import Node, Cluster, Provider, Region, Flavor, User
from rest_registration.models import RegistrationProfile
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin


class NodeInline(admin.StackedInline):
    model = Node
    extra = 0


class ClusterAdmin(SimpleHistoryAdmin):
    inlines = [NodeInline]
    list_display = ('__unicode__', 'user', 'cluster_size')

    def cluster_size(self, cluster):
        return cluster.nodes.count()

    cluster_size.short_description = 'Number of Nodes'


class RegionInline(admin.StackedInline):
    model = Region
    extra = 0


class FlavorInline(admin.StackedInline):
    model = Flavor
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    inlines = [RegionInline, FlavorInline]


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Node, SimpleHistoryAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(User)
admin.site.register(RegistrationProfile)
