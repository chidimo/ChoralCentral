"""Sitemap"""

from django.contrib.sitemaps import Sitemap

from .models import SiteUser

class SiteUserSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return SiteUser.objects.all()

    def lastmod(self, obj):
        return obj.modified
