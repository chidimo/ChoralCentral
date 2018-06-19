from django.contrib import admin

from .models import Url301

class Url301Admin(admin.ModelAdmin):
    list_display = ('app_name', 'new_reference', 'old_reference', 'created')

admin.site.register(Url301, Url301Admin)
