"""Feeds"""
# https://validator.w3.org/feed/docs/rss2.html
# https://goonan.io/podcast-feeds-in-django/
import os

from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import Song
from song_media.models import Midi

class MidiFeed(Feed):
    link = "http://www.choralcentral.net/"
    author_name = 'Chidi Orji'
    author_email = 'orjichidi95@gmail.com'
    categories = ("music", "midi", "choral", "choir", "scores")

    def description(self):
        return "Midi feed from http://www.choralcentral.net/"

    def title(self):
        return "Midis on ChoralCentral"

    def item_enclosure_url(self, item):
        return 'http://www.choralcentral.net{}'.format(item.media_file.url)

    def item_enclosure_length(self, item):
        return os.path.getsize(
            os.path.abspath(settings.BASE_DIR + item.media_file.url))

    def item_enclosure_mime_type(self):
        return 'audio/mpeg'

    def item_link(self, item):
        return 'http://www.choralcentral.net{}'.format(item.get_absolute_url())

    def items(self):
        return Midi.objects.all()

    def item_title(self, item):
        return '{}_{}'.format(item.song.title, item.part.name)

    def item_description(self, item):
        return item.song.lyrics

class SongFeed(Feed):
    link = "http://www.choralcentral.net/"
    categories = ("music", "midi", "choral", "choir", "scores")

    def get_object(self, request, feed_type):
        if feed_type == 'latest':
            return '-created', 'latest'
        else: # popular
            return '-like_count', 'popular'

    def description(self, obj):
        if obj[1] == 'popular':
            return "Most popular songs on http://www.choralcentral.net/"
        else:
            return "Most recent songs on http://www.choralcentral.net/"

    def item_link(self, item):
        return 'http://www.choralcentral.net{}'.format(item.get_absolute_url())

    def title(self, obj):
        if obj[1] == 'popular':
            return 'Popular on ChoralCentral'
        else:
            return 'Latest on ChoralCentral'

    def items(self, obj):
        return Song.published_set.all().order_by(obj[0])[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return "/n".join([str(item.like_count), item.first_line, item.scripture_reference, item.lyrics])
