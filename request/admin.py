"""Admin"""

from django.contrib import admin
from .models import Request, Reply

class RequestAdmin(admin.ModelAdmin):
    list_display = ("request", "status")
    search_fields = ("request", )

admin.site.register(Request, RequestAdmin)
admin.site.register(Reply)
