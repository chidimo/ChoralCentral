from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

blog_api_urls = [
    path('comment/', views.CommentViewSet.as_view({'get': 'list'}), name='comments_api'),
    path('post/', views.PostViewSet.as_view({'get': 'list'}), name='posts_api'),
]
