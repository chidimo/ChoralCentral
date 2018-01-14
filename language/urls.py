"""urls"""

from django.urls import path
from . import views

app_name = "language"
urlpatterns = [
    path("new", views.LanguageCreate.as_view(), name="new"),
    path("edit/<int:pk>/", views.LanguageEdit.as_view(), name="edit"),
    path("view/<int:pk>/", views.LanguageDetail.as_view(), name="detail"),
    path("delete/<int:pk>/", views.LanguageDelete.as_view(), name='delete'),
]