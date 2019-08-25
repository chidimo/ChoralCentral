from __future__ import unicode_literals

from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from song import views as songviews
from song_media import views as mediaviews
from author import views as authorviews
from siteuser import views as suviews

router = routers.DefaultRouter()
router.register('songs', songviews.SongViewSet)
router.register('voices', songviews.VoicesViewSet)
router.register('languages', songviews.LanguageViewSet)
router.register('mass-parts', songviews.MassPartViewSet)
router.register('seasons', songviews.SeasonViewSet)

router.register('voice-parts', mediaviews.VocalPartViewSet)
router.register('notation', mediaviews.ScoreNotationViewSet)
router.register('scores', mediaviews.ScoreViewSet)
router.register('midis', mediaviews.MidiViewSet)
router.register('videolinks', mediaviews.VideoLinkViewSet)

router.register('authors', authorviews.AuthorViewSet)

router.register('users', suviews.SiteUserViewSet)
router.register('custom-users', suviews.CustomUserViewSet)

urlpatterns = router.urls
