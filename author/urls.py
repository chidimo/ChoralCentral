"""urls"""

from django.urls import path
from . import views

app_name = "author"
urlpatterns = [
    path("", views.AuthorIndex.as_view(), name="index"),
    path("new/", views.NewAuthor.as_view(), name="new"),
    path("edit/<int:pk>/<slug:slug>/", views.AuthorEdit.as_view(), name="edit"),
    path("detail/<int:pk>/<slug:slug>", views.AuthorDetail.as_view(), name="detail"),
    path("delete/<int:pk>/", views.DeleteAuthor.as_view(), name='delete'),
]