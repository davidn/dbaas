#!/usr/bin/python
from __future__ import unicode_literals
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token
from .models import Node, Cluster, Provider, Region, Flavor, User, Backup
from rest_registration.models import RegistrationProfile
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from django.db import transaction
from django.conf import settings
from .forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm, AddDatabaseForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .controller import launch_cluster, pause_node, resume_node, reinstantiate_node, add_database, shutdown_cluster, \
    shutdown_node
from logging import getLogger

logger = getLogger(__name__)

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class NodeInline(admin.StackedInline):
    model = Node
    extra = 0
    exclude = ('lbr_region',)


class ClusterAdmin(SimpleHistoryAdmin):
    inlines = [NodeInline]
    list_display = ('__unicode__', 'user', 'cluster_size','status')
    list_filter = ('user', 'status')
    actions = ('launch','shutdown')

    def get_urls(self):
        from django.conf.urls import patterns

        return patterns('',
                        (r'^(.+)/add_database/$',
                         self.admin_site.admin_view(self.add_database))
        ) + super(ClusterAdmin, self).get_urls()

    def cluster_size(self, cluster):
        return cluster.nodes.count()

    cluster_size.short_description = 'Number of Nodes'

    def launch(self, request, queryset):
        for cluster in queryset:
            launch_cluster(cluster)

    def shutdown(self, request, queryset):
        for cluster in queryset:
            shutdown_cluster(cluster)

    def add_database(self, request, cluster_id, form_url='', extra_context=None):
        if not self.has_change_permission(request):
            raise PermissionDenied
        cluster = get_object_or_404(self.queryset(request), pk=cluster_id)
        if request.method == 'POST':
            form = AddDatabaseForm(request.POST)
            if form.is_valid():
                add_database(cluster, form.cleaned_data['database'])
                messages.success(request, 'Databased Added')
                return HttpResponseRedirect('..')
        else:
            form = AddDatabaseForm()
        fieldsets = [(None, {'fields': list(form.base_fields)})]
        admin_form = admin.helpers.AdminForm(form, fieldsets, {})
        context = {
            'title': _('Add Database: %s') % escape(str(cluster)),
            'adminform': admin_form,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': False,
            'change': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_add_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': cluster,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(request, 'add_database.html', context=context, current_app=self.admin_site.name)


class NodeAdmin(SimpleHistoryAdmin):
    exclude = ('lbr_region',)
    actions = ('pause', 'resume', 'shutdown')
    list_display = ('__unicode__', 'cluster_user', 'region', 'flavor', 'status', 'ip')
    list_filter = ('region', 'cluster', 'status', 'region__provider')

    def cluster_user(self, node):
        return node.cluster.user

    def pause(self, request, queryset):
        for node in queryset:
            pause_node(node)

    def resume(self, request, queryset):
        for node in queryset:
            resume_node(node)

    def shutdown(self, request, queryset):
        for node in queryset:
            shutdown_node(node)

    def save_model(self, request, obj, form, change):
        node = Node.objects.get(pk=obj.pk)
        # Persist everything but the flavor,
        # the flavor will be modified as a result of resizing the Node.
        new_flavor = obj.flavor
        obj.flavor = node.flavor
        obj.save()
        # Apply the Node resizing if the flavor changed.
        if new_flavor.code != node.flavor.code:
            logger.info("Resizing node %s from %s to %s" % (str(obj), obj.flavor.name, new_flavor.name))
            reinstantiate_node(obj, new_flavor)


class BackupAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'node', 'time', 'size')
    list_filter = ('node', 'node__cluster', 'node__cluster__user')


class RegionInline(admin.StackedInline):
    model = Region
    extra = 0


class FlavorInline(admin.StackedInline):
    model = Flavor
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    inlines = [RegionInline, FlavorInline]


class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_paid', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_paid', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls import patterns

        return patterns('', (r'^(\d+)/password/$',
                        self.admin_site.admin_view(self.user_change_password))) + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        admin_form = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': admin_form,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(request,
                                self.change_user_password_template or
                                'admin/auth/user/change_password.html',
                                context, current_app=self.admin_site.name)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(UserAdmin, self).response_add(request, obj,
                                                   post_url_continue)


class TokenImpersonationAdmin(TokenAdmin):
    list_display = ('key', 'user', 'impersonate', 'created')

    readonly_fields = ('impersonate',)

    def impersonate(self, instance):
        return "<a href=" + settings.FRONTEND_URL + '#/impersonate/' + instance.key + ">Impersonate User</a>"

    # short_description functions like a model field's verbose_name
    impersonate.short_description = "Impersonation"
    # in this example, we have used HTML tags in the output
    impersonate.allow_tags = True


admin.site.register(Backup, BackupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(RegistrationProfile)
admin.site.unregister(Token)
admin.site.register(Token, TokenImpersonationAdmin)
