"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Song

class SongSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Song.published_set.all()

    def lastmod(self, obj):
        return obj.modified