"""urls"""

from django.urls import path
from . import views
from .feeds import LatestPostSFeed

app_name = "blog"
urlpatterns = [
    path('', views.PostIndex.as_view(), name="index"),
    path("new/", views.NewPost.as_view(), name="new"),
    path("<int:pk>/<slug:slug>/", views.post_detail_view, name="detail"),
    path("new/from/<int:pk>/", views.NewPostFromSong.as_view(), name="new_song"),
    path("edit/<int:pk>/", views.PostEdit.as_view(), name="edit"),
    path("post-moved/<int:pk>/<slug:slug>/", views.post_redirect_301_view, name="post_moved"),

    path("share-email/<int:pk>/<slug:slug>/", views.share_post_by_mail, name='share_post_by_mail'),
    path("like/", views.post_like_view, name='like_post'),
]

urlpatterns += [
    path("edit-comment/<int:pk>/", views.EditComment.as_view(), name="edit_comment"),
    path("delete-comment/<int:pk>/", views.DeleteComment.as_view(), name="comment_delete"),
    path("reply/<int:comment_pk>/<int:post_pk>/", views.ReplyComment.as_view(), name="comment_reply"),
]

urlpatterns += [
    path("feed/", LatestPostSFeed(), name="post_feed"),
    path("instant-search/", views.instant_blog, name="instant_blog"),
    path("auto-complete/", views.auto_blog, name="auto_blog"),
]

