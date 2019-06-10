from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from vault.models import User, Credential, SecureNote

admin.site.site_header = 'Passman Admin Panel'
admin.site.site_title = 'Passman Admin Panel'
admin.site.index_title = 'Dashboard'


@admin.register(User)
class AdminUserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    add_form_template = 'admin/auth/user/add_form.html'
    fieldsets = (
        [None, {'fields': ['email', 'password']}],
        (_('Personal info'), {'fields': ['first_name', 'last_name']}),
        [_('Permissions and status'),
         {'fields': ['is_active', 'is_staff', 'is_superuser']}],
        [_('Important dates'), {'fields': ('last_login_display', 'date_joined_display')}],
    )
    add_fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2'],
        }],
    ]
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_superuser', 'is_staff']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['email']
    readonly_fields = ['last_login_display', 'date_joined_display']

    def last_login_display(self, obj):
        if None:
            return '-'
        else:
            return datetime.strftime(obj.last_login, '%a %b %d, %Y')

    last_login_display.short_description = _('date created')

    def date_joined_display(self, obj):
        if None:
            return '-'
        else:
            return datetime.strftime(obj.date_joined, '%a %b %d, %Y')

    date_joined_display.short_description = _('date created')


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ['name', 'owner_name', 'date_created_display']
    list_filter = ['owner']
    search_fields = ['name', 'owner']

    def get_queryset(self, request):
        query = super(CredentialAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            qs = query.all()
        else:
            qs = query.filter(owner=request.user)
        return qs

    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
            [None, {'fields': ['name', 'username', 'password', 'url']}],
            [_('Important dates'), {'fields': ['date_created_display']}],
        ]

        if request.user.is_superuser:
            self.fieldsets[0][1].get('fields').insert(0, 'owner')
        elif obj:
            self.fieldsets[0][1].get('fields').insert(0, 'owner_name')
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['date_created_display']

        if not request.user.is_superuser or obj:
            self.readonly_fields.insert(0, 'owner_name')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user

        super(CredentialAdmin, self).save_model(request, obj, form, change)

    def owner_name(self, obj):
        full_name = obj.owner.get_full_name()
        return full_name if full_name else obj.owner.email

    owner_name.short_description = _('owner')

    def date_created_display(self, obj):
        if None:
            return '-'
        else:
            return datetime.strftime(obj.date_created, '%a %b %d, %Y')

    date_created_display.short_description = _('date created')


@admin.register(SecureNote)
class SecureNoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ['title', 'owner_name', 'date_created_display']
    list_filter = ['owner']
    search_fields = ['title', 'owner']

    def get_queryset(self, request):
        query = super(SecureNoteAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            qs = query.all()
        else:
            qs = query.filter(owner=request.user)
        return qs

    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
            [None, {'fields': ['title', 'note']}],
            [_('Important dates'), {'fields': ['date_created_display']}],
        ]

        if request.user.is_superuser:
            self.fieldsets[0][1].get('fields').insert(0, 'owner')
        elif obj:
            self.fieldsets[0][1].get('fields').insert(0, 'owner_name')
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['date_created_display']

        if not request.user.is_superuser or obj:
            self.readonly_fields.insert(0, 'owner_name')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user

        super(SecureNoteAdmin, self).save_model(request, obj, form, change)

    def owner_name(self, obj):
        full_name = obj.owner.get_full_name()
        return full_name if full_name else obj.owner.email

    owner_name.short_description = _('owner')

    def date_created_display(self, obj):
        if None:
            return '-'
        else:
            return datetime.strftime(obj.date_created, '%a %b %d, %Y')

    date_created_display.short_description = _('date created')
