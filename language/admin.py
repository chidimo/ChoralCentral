"""admin"""

from django.contrib import admin
from .models import Language

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language", )

admin.site.register(Language, LanguageAdmin)
