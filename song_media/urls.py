"""urls"""

from django.urls import path
from . import views

app_name = "song-media"
urlpatterns = [
    path("new/sheet/", views.SheetAdd.as_view(), name="sheet_add"),
    path("new/sheet/<int:pk>/", views.SheetAdd.as_view(), name="sheet_add_song"),
    path("view/sheet/<int:pk>/", views.DisplaySheet.as_view(), name="sheet_view"),
]

urlpatterns += [
    path("new/midi/", views.MidiAdd.as_view(), name="midi_add"),
    path("new/midi/<int:pk>/", views.MidiAdd.as_view(), name="midi_add_song"),
    path("play/midi/<int:pk>/", views.PlayMidi.as_view(), name="play_midiview"),
]

urlpatterns += [
    path("new/video/", views.VideoLinkAdd.as_view(), name="videolink_new"),
    path("new/video/<int:pk>/", views.VideoLinkAdd.as_view(), name="videolink_new_song"),
]