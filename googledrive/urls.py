from django.urls import path
from . import views

app_name = 'googledrive'

urlpatterns = [
    path('googledrive/', views.authorize_drive, name='authorize_drive'),
    path('callback/', views.callback, name='drive_callback_url'),
]