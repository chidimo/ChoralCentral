"""admin"""

from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "author_type", "creator")

admin.site.register(Author, AuthorAdmin)
