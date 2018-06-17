"""Admin"""

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Role, SiteUser, SiteUserGroup, GroupMembership, GroupJoinRequest, Badge, Message, SiteUserPermission
from .forms import UserChangeForm, UserCreationForm

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "user", "first_name", "last_name", "slug", "location", "key", "quota", "used", "remaining_quota")
    list_editable = ('location', )

class FollowAdmin(admin.ModelAdmin):
    list_display = ("from_siteuser", "to_siteuser", "created")

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hierarchy', 'description', 'color')
    list_editable = ('color', )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('read', 'sender', 'receiver', 'body', 'thread_id')
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
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(SiteUserPermission, SiteUserPermissionAdmin)

admin.site.unregister(Group)
