"""urls"""

from django.urls import path
from . import views
from . import feeds


app_name = "song"

urlpatterns = [
    path("new/", views.NewVoicing.as_view(), name="new"),
    path("edit/<int:pk>/", views.VoicingEdit.as_view(), name="edit"),
]

urlpatterns += [
    path('', views.SongIndex.as_view(), name="index"),
    path("new/", views.NewSong.as_view(), name="new"),
    path("edit/<int:pk>/<slug:slug>/", views.SongEdit.as_view(), name="edit"),
    path("filter/", views.FilterSongs.as_view(), name="filter"),
    path("<int:pk>/<slug:slug>/", views.SongDetail.as_view(), name="detail"),
    path("<int:pk>/<slug:slug>/reader/", views.reader_view, name="reader"),
    path("delete/<int:pk>/", views.SongDelete.as_view(), name='delete'),
]

urlpatterns += [
    path("like/", views.song_like_view, name='like_song'),
    path("reader/<int:pk>/<slug:slug>/", views.reader_view, name='reader_view'),
    path("share-email/<int:pk>/<slug:slug>/", views.share_song_by_mail, name='share_song_by_mail'),
    path("share-facebook/<int:pk>/<slug:slug>/", views.share_on_facebook, name='share_on_facebook'),
]

urlpatterns += [
    path("feed-<str:feed_type>/", feeds.SongFeed(), name="song_feed"),
    path("midi-feed/", feeds.MidiFeed(), name="midi_feed"),
    path("instant-search/", views.InstantSong.as_view(), name="instant_song"),
    path("auto-complete/", views.auto_song, name="auto_song"),
]