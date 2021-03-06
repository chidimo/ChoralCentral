"""urls"""

from django.urls import path
from . import views

app_name = 'song-media'
urlpatterns = [
    path('new-score/song-<int:pk>/', views.NewScore.as_view(), name='score_add_to_song'),
    path('view-score/<int:pk>/', views.show_score, name='show_score'),
]

urlpatterns += [
    path('new-sound/song-<int:pk>/', views.NewMidi.as_view(), name='midi_add_to_song'),
    path('play-mp3/<int:pk>/', views.play_mp3, name='playmp3'),
    path('download-sound/<int:pk>/', views.download_midi, name='download_midi'),
]

urlpatterns += [
    path('score-delete/<int:pk>/', views.DeleteScore.as_view(), name="delete_score"),
    path('sound-delete/<int:pk>/', views.DeleteMidi.as_view(), name="delete_midi"),
]

urlpatterns += [
    path('new/video/', views.NewVideoLink.as_view(), name='videolink_new'),
    path('new-video/song-<int:pk>/', views.NewVideoLink.as_view(), name='add_videolink_to_song'),
]

urlpatterns += [
    path('new/part/', views.NewVocalPart.as_view(), name='new_part'),
    path('new/notation/', views.NewScoreNotation.as_view(), name='new_notation'),
]