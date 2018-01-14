"""Feeds"""

from django.db.models import Count
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Song

class PopularSongFeed(Feed):
    title = "Song"
    link = "/song/"
    description = "Get the latest update."

    def items(self):
        return Song.published_set.all().annotate(Count("likes")).order_by("-likes__count")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "/n".join([item.first_line, item.scripture_ref])

class LatestSongFeed(Feed):
    title = "Song"
    link = "/song/"
    description = "Get the latest update."

    def items(self):
        return Song.published_set.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "/n".join([item.first_line, item.scripture_ref])
