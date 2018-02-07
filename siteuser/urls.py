"""urls live here"""

from django.urls import path
from . import views
from django.contrib.auth import views as account_views

app_name = "siteuser"
urlpatterns = [
    path('', views.SiteUserIndex.as_view(), name="index"),
    path("new/", views.new_siteuser, name="new"),
    path("edit/<int:pk>/<slug:slug>/", views.SiteUserEdit.as_view(), name="edit"),
    path("welcome/<str:screen_name>/", views.welcome_siteuser, name="new_success"),
    path("activate/<int:pk>/<str:screen_name>/", views.activate_siteuser, name="new_activation"),
    path("<int:pk>/<slug:slug>/", views.SiteUserDetail.as_view(), name="detail"),
    path("<int:pk>/comments/", views.SiteUserComments.as_view(), name="comments"),
]

urlpatterns += [
    path("new-role/", views.NewRole.as_view(), name="role_create"),
    path("view/roles/", views.RoleIndex.as_view(), name="role_index"),
]


urlpatterns += [
    path("login/", account_views.login, name="login"),
    path("logout/", account_views.logout, name="logout"),
    path("logout-then-login/", account_views.logout_then_login, name="logout_then_login"),

    path("change-password/", account_views.password_change, name="change_password"),
    path("change-password/done/", account_views.password_change_done, name="change_password_dong"),

    path("reset-password/", account_views.password_reset, name="reset_password"),
    path("reset-password/done/", account_views.password_reset_done, name="reset_password_done"),
    path("reset-password/confirm/", account_views.password_reset_confirm, name="reset_password_confirm"),
    path("reset-password/complete/", account_views.password_reset_complete, name="reset_password_complete"),
]
