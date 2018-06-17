"""Admin"""

from django.contrib import admin
from .models import Request, Reply

class RequestAdmin(admin.ModelAdmin):
    list_display = ("title", "status")
    search_fields = ("title", )

admin.site.register(Request, RequestAdmin)
admin.site.register(Reply)
