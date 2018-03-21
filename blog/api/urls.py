from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, 'Published posts')
router.register(r'comments', views.CommentViewSet, 'All comments')
router.register(r'comments-user', views.UserCommentViewSet, 'User comments')

blog_api_urls = [
    path('post/', views.PostViewSet.as_view({'get': 'list'}), name='posts_api'),
    path('comment/', views.CommentViewSet.as_view({'get': 'list'}), name='comments_api'),
    path('comment/<int:pk>/', views.UserCommentViewSet.as_view({'get': 'list'}), name='user_comments_api'),
]
