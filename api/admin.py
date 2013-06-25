from .models import Node, Cluster
from django.contrib import admin


class NodeInline(admin.StackedInline):
    model=Node
    extra=0

class ClusterAdmin(admin.ModelAdmin):
    inlines = [NodeInline]
    list_display = ('__unicode__', 'user', 'cluster_size')

    def cluster_size(self, cluster):
        return cluster.node_set.count()
    cluster_size.short_description = 'Number of Nodes'


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Node)
