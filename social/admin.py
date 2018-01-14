from django.contrib import admin

from .models import Favorite, Collection

admin.site.register(Favorite)
admin.site.register(Collection)
