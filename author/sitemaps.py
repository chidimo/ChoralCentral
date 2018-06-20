"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Author

class AuthorSiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Author.objects.all()

    def lastmod(self, obj):
        return obj.modified
