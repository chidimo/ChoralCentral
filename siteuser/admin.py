"""Admin"""
import pprint
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Role, SiteUser, Message, SiteUserPermission, ApiKey
from .forms import UserChangeForm, UserCreationForm

from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ('session_key', '_session_data', 'expire_date')

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ("pk", "screen_name", "user", "first_name", "last_name", 'all_roles', "slug", "location", "quota", "used", "remaining_quota")
    # list_editable = ('location', )

    def all_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

class MessageAdmin(admin.ModelAdmin):
    list_display = ('read', 'creator', 'receiver', 'body', 'thread_id')
    list_editable = ('thread_id', )

class SiteUserPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'permitted_siteusers')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'is_active', "siteuser")
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields' : ('email', 'password')}),
        ('Personal info', {'fields' : ()}),
        ('Permissions', {'fields' : ('is_admin', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Message, MessageAdmin)
admin.site.register(SiteUserPermission, SiteUserPermissionAdmin)
admin.site.register(ApiKey)

admin.site.unregister(Group)
admin.site.register(Session, SessionAdmin)
