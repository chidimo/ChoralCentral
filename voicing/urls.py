"""urls"""

from django.urls import path
from . import views

app_name = "voicing"
urlpatterns = [
    path("new/", views.NewVoicing.as_view(), name="new"),
    path("edit/<int:pk>/", views.VoicingEdit.as_view(), name="edit"),
]