"""urls"""

from django.urls import path
from . import views

app_name = 'song-media'
urlpatterns = [
    path('new/score/', views.NewScore.as_view(), name='score_add'),
    path('new/score/<int:pk>/', views.NewScore.as_view(), name='score_add_song'),
    path('view/score/<int:pk>/', views.DisplayScore.as_view(), name='score_view'),
]

urlpatterns += [
    path('new/midi/', views.MidiAdd.as_view(), name='midi_add'),
    path('new/midi/<int:pk>/', views.MidiAdd.as_view(), name='midi_add_song'),
    path('play/midi/<int:pk>/', views.PlayMidi.as_view(), name='play_midiview'),
]

urlpatterns += [
    path('new/video/', views.VideoLinkAdd.as_view(), name='videolink_new'),
    path('new/video/<int:pk>/', views.VideoLinkAdd.as_view(), name='videolink_new_song'),
]

urlpatterns += [
    path('new/part/', views.NewVocalPart.as_view(), name='new_part'),
    path('new/notation/', views.NewScoreNotation.as_view(), name='new_notation'),
]