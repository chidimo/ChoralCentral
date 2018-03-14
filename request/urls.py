"""Docstring"""

from django.urls import path
from . import views

# pylint: disable=C0326, C0301, C0103, C0111

app_name = "request"
urlpatterns = [
    path('', views.RequestIndex.as_view(), name="index"),
    path("new/", views.RequestCreate.as_view(), name="new"),
    path("edit/<int:pk>/", views.RequestEdit.as_view(), name="edit"),
    path("detail/<int:pk>/<slug:slug>/", views.RequestDetail.as_view(), name="detail"),
    path("sort/", views.FilterRequests.as_view(), name="filter"),
]

urlpatterns += [
    path("reply/request/<int:pk>/", views.ReplyAddFromRequest.as_view(), name="reply_new_from_request"),
    path("replys/", views.ReplyIndex.as_view(), name="reply_index"),
]