"""urls"""

from django.urls import path
from . import views

app_name = 'song-media'
urlpatterns = [
    path('new/score/', views.NewScore.as_view(), name='new_score'),
    path('new/score/<int:pk>/', views.NewScore.as_view(), name='score_add_song'),
    path('view/score/<int:pk>/', views.DisplayScore.as_view(), name='score_view'),
]

urlpatterns += [
    path('new/midi/', views.NewMidi.as_view(), name='midi_add'),
    path('new/midi/<int:pk>/', views.NewMidi.as_view(), name='midi_add_song'),
    path('play/midi/<int:pk>/', views.PlayMidi.as_view(), name='play_midiview'),
]

urlpatterns += [
    path('score/delete/<int:pk>/<int:song_pk>/<slug:slug>/', views.DeleteScore.as_view(), name="delete_score"),
    path('midi/delete/<int:pk>/<int:song_pk>/<slug:slug>/', views.DeleteMidi.as_view(), name="delete_midi"),
]

urlpatterns += [
    path('new/video/', views.NewVideoLink.as_view(), name='videolink_new'),
    path('new/video/<int:pk>/', views.NewVideoLink.as_view(), name='videolink_new_song'),
]

urlpatterns += [
    path('new/part/', views.NewVocalPart.as_view(), name='new_part'),
    path('new/notation/', views.NewScoreNotation.as_view(), name='new_notation'),
]