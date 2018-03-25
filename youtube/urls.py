from django.urls import path
from . import views

app_name = 'youtube'

urlpatterns = [
    path('youtube/', views.get_youtube_permissions, name='get_youtube_permissions'),
    path('youtube-callback/', views.youtube_callback, name='youtube_callback'),
]