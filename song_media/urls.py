"""urls"""

from django.urls import path
from . import views

app_name = 'song-media'
urlpatterns = [
    path('media-index/', views.admin_media_index, name='admin_media_index'),
    path('new-score/', views.NewScore.as_view(), name='new_score'),
    path('new-score-<int:pk>/', views.NewScore.as_view(), name='score_add_song'),
    path('view-score/<int:pk>/', views.show_score, name='show_score'),
    path('download-score-drive-<int:pk>/', views.download_score_from_drive, name='download_score_from_drive'),
    path('download-midi-drive-<int:pk>/', views.download_midi_from_drive, name='download_midi_from_drive'),
]

urlpatterns += [
    path('new/sound/', views.NewMidi.as_view(), name='midi_add'),
    path('new/sound/<int:pk>/', views.NewMidi.as_view(), name='midi_add_song'),
    path('sound/play/<int:pk>/', views.play_mp3, name='play_midiview'),
    path('download/midi/<int:pk>/', views.download_midi, name='download_midi'),
]

urlpatterns += [
    path('score/delete/<int:pk>/', views.DeleteScore.as_view(), name="delete_score"),
    path('sound/delete/<int:pk>/', views.DeleteMidi.as_view(), name="delete_midi"),
]

urlpatterns += [
    path('new/video/', views.NewVideoLink.as_view(), name='videolink_new'),
    path('new/video/<int:pk>/', views.NewVideoLink.as_view(), name='videolink_new_song'),
]

urlpatterns += [
    path('new/part/', views.NewVocalPart.as_view(), name='new_part'),
    path('new/notation/', views.NewScoreNotation.as_view(), name='new_notation'),
]