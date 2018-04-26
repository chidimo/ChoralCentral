"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(publish=True)

    def lastmod(self, obj):
        return obj.modified
