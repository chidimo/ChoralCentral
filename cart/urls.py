"""urls live here"""

from django.urls import path
from . import views

# pylint: disable=C0326, C0301, C0103, C0111

app_name = "cart"
urlpatterns = [
    path('', views.cart_detail, name="detail"),
    path("add/<int:song_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:song_id>/", views.remove_to_cart, name="remove_to_cart"),
]
