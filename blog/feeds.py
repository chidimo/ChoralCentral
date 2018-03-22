"""Feeds"""

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post

class LatestPostSFeed(Feed):
    title = "Blog"
    link = "/blog/"
    description = "Get the latest update."

    def items(self):
        return Post.objects.filter(publish=True).order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle

