from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'songs', views.VerseListView, 'Verses list')
router.register(r'songs', views.VerseDetailView, 'Verse details')
router.register(r'songs', views.ChapterListView, 'Chapters')
router.register(r'songs', views.CommentaryTextListView, 'Commentary text')

drb_api_urls = [
    path('verse/', views.VerseListView.as_view(), name="verses"),
    path('verse-detail/<int:pk>/', views.VerseDetailView.as_view(), name="verse_detail"),
    path('chapters/', views.ChapterListView.as_view(), name="chapters"),
    path('commentary/', views.CommentaryTextListView.as_view(), name="commentaries"),
]
