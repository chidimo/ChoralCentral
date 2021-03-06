"""urls"""

from django.urls import path
from . import views
from . import feeds

app_name = "song"

urlpatterns = [
    path("new-voicing/", views.NewVoicing.as_view(), name="new_voicing"),
    path("edit-voicing/<int:pk>/", views.VoicingEdit.as_view(), name="edit_voicing"),
    path("song-moved/<int:pk>/<slug:slug>/", views.song_redirect_301_view, name="song_moved"),
]

urlpatterns += [
    path("new-language/", views.NewLanguage.as_view(), name="new_language"),
    path("edit-language/<int:pk>/", views.LanguageEdit.as_view(), name="edit_language"),
    path("view/<int:pk>/", views.LanguageDetail.as_view(), name="detail"),
    path("delete-language/<int:pk>/", views.LanguageDelete.as_view(), name='delete'),
    path("publish-shortcut/<int:pk>/", views.publish_song_shortcut, name="publish_song_shortcut"),
]

urlpatterns += [
    path('', views.SongIndex.as_view(), name="song_index"),
    path("new-song/", views.NewSong.as_view(), name="new"),
    path('ajax/check-song-exists/', views.check_song_exists, name='check_song_exists'),
    path("edit-song/<int:pk>/<slug:slug>/", views.SongEdit.as_view(), name="edit"),
    path("song/<int:pk>/<slug:slug>/", views.song_detail_view, name="detail"),
    path("song/<int:pk>/<slug:slug>/reader/", views.reader_view, name="reader"),
    path("delete-song/<int:pk>/", views.SongDelete.as_view(), name='delete'),
]

urlpatterns += [
    path("reader/<int:pk>/<slug:slug>/", views.reader_view, name='reader_view'),
    path("share-email/<int:pk>/<slug:slug>/", views.share_song_by_mail, name='share_song_by_mail'),
]

urlpatterns += [
    path("feed-<str:feed_type>/", feeds.SongFeed(), name="song_feed"),
    path("midi-feed/", feeds.MidiFeed(), name="midi_feed"),
    path("song-search/", views.InstantSong.as_view(), name="instant_search_song"),
    path("auto-complete/", views.auto_song, name="auto_song"),
]
