"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Request

class RequestSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Request.objects.all()

    def lastmod(self, obj):
        return obj.modified
