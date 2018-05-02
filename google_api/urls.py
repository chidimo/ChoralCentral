from django.urls import path
from . import views

app_name = 'google-api'

urlpatterns = []

urlpatterns += [
    path('drive/', views.drive_authorize, name='drive_authorize'),
    path('drive-callback/', views.drive_callback, name='drive_callback'),
]

urlpatterns += [
    path('youtube/', views.youtube_authorize, name='youtube_authorize'),
    path('youtube-callback/', views.youtube_callback, name='youtube_callback'),
]