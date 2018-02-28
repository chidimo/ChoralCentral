"""Feeds"""

from django.db.models import Count
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Song

class PopularSongFeed(Feed):
    title = "ChoralCentral"
    link = "/song/"
    description = "Catch the most popular scores on http://choralcentral.net/"

    def items(self):
        return Song.published_set.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "/n".join([item.first_line, item.scripture_reference, item.lyrics])

class LatestSongFeed(Feed):
    title = "ChoralCentral"
    link = "/song/"
    description = "Catch the latest scores on http://choralcentral.net/."

    def items(self):
        return Song.published_set.all()[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "/n".join([item.first_line, item.scripture_reference, item.lyrics])
