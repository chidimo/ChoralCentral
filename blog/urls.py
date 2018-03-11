"""urls live here"""

from django.urls import path
from . import views
from .feeds import LatestPostSFeed

# pylint: disable=C0326, C0301, C0103, C0111

app_name = "blog"
urlpatterns = [
    path('', views.PostIndex.as_view(), name="index"),
    path("new/", views.PostCreate.as_view(), name="new"),
    path("<int:pk>/<slug:slug>/", views.PostDetail.as_view(), name="detail"),
    path("new/from/<int:pk>/", views.PostCreateFromSong.as_view(), name="new_song"),
    path("edit/<int:pk>/", views.PostEdit.as_view(), name="edit"),
    path("share-email/<int:pk>/<slug:slug>/", views.share_post_by_mail, name='share_post_by_mail'),
    path("like/", views.post_like_view, name='like_post'),
]

urlpatterns += [
    path("new/comment/<int:pk>/", views.CommentCreate.as_view(), name="comment_add"),
    path("edit/comment/<int:pk>/", views.EditComment.as_view(), name="comment_edit"),
    path("reply/<int:comment_pk>/<int:post_pk>/", views.ReplyComment.as_view(), name="comment_reply"),
]

urlpatterns += [
    path("feed/", LatestPostSFeed(), name="post_feed"),
    path("instant-search/", views.instant_blog, name="instant_blog"),
    path("auto-complete/", views.auto_blog, name="auto_blog"),
]