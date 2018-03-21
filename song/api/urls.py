from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'songs', views.PublishedSongViewSet, 'Published songs')
router.register(r'songs', views.UnpublishedSongViewSet, 'Unpublished songs')
router.register(r'songs', views.PublishedAuthorSongViewSet, 'Author published songs')

song_api_urls = [
    path('song-published/', views.PublishedSongViewSet.as_view({'get': 'list'}), name='song_published_api'),
    path('song-unpublished/', views.UnpublishedSongViewSet.as_view({'get': 'list'}), name='song_unpublished_api'),
    path('song-author-published/<int:pk>/<slug:slug>/', views.PublishedAuthorSongViewSet.as_view({'get': 'list'}), name='published_author_api'),
]
