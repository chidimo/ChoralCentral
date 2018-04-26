"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Song

class SongSiteMap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Song.objects.filter(publish=True)

    def lastmod(self, obj):
        return obj.modified
