"""urls"""

from django.urls import path
from . import views

app_name = "todaymass"
urlpatterns = [
    path("new/", views.NewMass.as_view(), name="new"),
    path("add-to-mass/", views.AddToMass.as_view(), name="add_to_mass"),
    path("<int:pk>/", views.ViewMass.as_view(), name="detail"),
]
