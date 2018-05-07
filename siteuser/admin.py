"""Admin"""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Role, SiteUser, SiteUserGroup, GroupMembership, GroupJoinRequest, Follow
from .forms import UserChangeForm, UserCreationForm

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "user", "first_name", "last_name", "slug", "location", "key", "quota", "remaining", )

class FollowAdmin(admin.ModelAdmin):
    list_display = ("from_siteuser", "to_siteuser", "created")

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'is_active', "prof")
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
admin.site.register(Follow, FollowAdmin)
admin.site.register(Role)

admin.site.unregister(Group)
