"""urls"""

from django.urls import path

from . import views
from . import feeds

# pylint: disable=C0326, C0301, C0103, C0111

app_name = "song"

urlpatterns = [
    path('', views.SongIndex.as_view(), name="index"),
    path("new/", views.NewSong.as_view(), name="new"),
    path("edit/<int:pk>/<slug:slug>/", views.SongEdit.as_view(), name="edit"),
    path("filter/", views.filter_songs, name="filter"),
    path("season/<str:season>", views.filter_season, name="filter_season"),
    path("masspart/<str:masspart>", views.filter_masspart, name="filter_masspart"),
    path("<int:pk>/<slug:slug>/", views.SongDetail.as_view(), name="detail"),
    path("<int:pk>/<slug:slug>/reader/", views.reader_view, name="reader"),
    path("delete/<int:pk>/", views.SongDelete.as_view(), name='delete'),
]

urlpatterns += [
    path("like_song/", views.song_like_view, name='like_song')
]

urlpatterns += [
    path("feed/latest/", feeds.LatestSongFeed(), name="latest_song_feed"),
    path("feed/popular/", feeds.PopularSongFeed(), name="popular_song_feed"),
    path("instant-search/", views.instant_song, name="instant_song"),
    path("auto-complete/", views.auto_song, name="auto_song"),
]