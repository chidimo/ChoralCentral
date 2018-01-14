"""Sitemap"""

from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.published_set.all()

    def last_mod(self, obj):
        return obj.modified
