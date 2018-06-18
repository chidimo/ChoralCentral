from django.contrib import admin

from .models import Url301

class Url301Admin(admin.ModelAdmin):
    list_display = ('new_url', 'old_url', 'created')

admin.site.register(Url301, Url301Admin)
