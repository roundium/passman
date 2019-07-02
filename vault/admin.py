from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from vault.models import User, Team, Credential, SecureNote

admin.site.site_header = _('Passman Admin Panel')
admin.site.site_title = _('Passman Admin Panel')
admin.site.index_title = _('Dashboard')


@admin.register(User)
class UserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    add_form_template = 'admin/auth/user/add_form.html'
    fieldsets = (
        [None, {'fields': ['email', 'password']}],
        (_('Personal info'), {'fields': ['first_name', 'last_name']}),
        [_('Permissions and status'),
         {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups']}],
        [_('Important dates'), {'fields': ('last_login', 'date_joined')}],
    )
    add_fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2'],
        }],
    ]
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_superuser', 'is_staff', 'groups']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['email']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fields = ['owner', 'name', 'members']
    list_display = ['name', 'owner']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super(TeamAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            return qs.filter(owner=request.user)

        return qs

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = []

        if not request.user.is_superuser or obj:
            self.readonly_fields.insert(0, 'owner')

        return self.readonly_fields


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    fieldsets = [
        [None, {'fields': ['owner', 'team', 'name', 'username', 'password', 'url']}],
        [_('Important dates'), {'fields': ['date_created']}],
    ]
    list_display = ['name', 'owner', 'date_created']
    list_filter = ['owner']
    search_fields = ['name', 'owner']

    def get_queryset(self, request):
        qs = super(CredentialAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            return qs.filter(
                Q(owner=request.user) | Q(team__owner=request.user) | Q(team__in=request.user.team_set.all()))

        return qs

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = []

        if not request.user.is_superuser or obj:
            self.readonly_fields.insert(0, 'owner')

            if not request.user == obj.owner:
                self.readonly_fields.insert(0, 'team')

        return self.readonly_fields


@admin.register(SecureNote)
class SecureNoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    fieldsets = [
        [None, {'fields': ['owner', 'team', 'title', 'note']}],
        [_('Important dates'), {'fields': ['date_created']}],
    ]
    list_display = ['title', 'owner', 'date_created']
    list_filter = ['owner']
    search_fields = ['title', 'owner']

    def get_queryset(self, request):
        qs = super(SecureNoteAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            return qs.filter(Q(owner=request.user) | Q(team__in=request.user.team_set.all()))

        return qs

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = []

        if not request.user.is_superuser or obj:
            self.readonly_fields.insert(0, 'owner')

            if not request.user == obj.owner:
                self.readonly_fields.insert(0, 'team')

        return self.readonly_fields
