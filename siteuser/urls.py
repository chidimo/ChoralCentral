"""urls live here"""

from django.urls import reverse_lazy, path
from django.contrib.auth import views as auth_views

from . import views

# app_name = "users"
app_name = "siteuser"

urlpatterns = [
    path('', views.SiteUserIndex.as_view(), name="index"),
    path('roles-<str:role>/', views.SiteUserCommonRoles.as_view(), name="siteusers_common_roles"),
    path("new/", views.new_siteuser, name="new"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("deactivate-account/", views.deactivate_account, name="deactivate_account"),
    path("activate-account/", views.activate_account, name="activate_account"),
    path("edit-profile/", views.SiteUserEdit.as_view(), name="edit_profile"),
    path("welcome/<str:screen_name>/", views.welcome_siteuser, name="new_success"),
    path("activate/<int:pk>/<str:screen_name>/", views.activate_siteuser, name="new_activation"),
    path("library/<int:pk>/<slug:slug>/", views.SiteUserLibrary.as_view(), name="library"),
    path("comments/<int:pk>/<slug:slug>/", views.SiteUserComments.as_view(), name="siteuser_comments"),
]

urlpatterns += [
    path("new-role/", views.NewRole.as_view(), name="role_create"),
    path("view/roles/", views.RoleIndex.as_view(), name="role_index"),
    path('song-love-birds/<int:pk>/<slug:slug>/', views.SongLoveBirds.as_view(), name='song_likers'),
    path('post-love-birds/<int:pk>/<slug:slug>/', views.PostLoveBirds.as_view(), name='post_likers'),
    path('comment-love-birds/<int:pk>/', views.CommentLoveBirds.as_view(), name='comment_likers'),
]

urlpatterns += [
    path('groups/', views.GroupIndex.as_view(), name='siteuser_groups'),
    path('new-group/', views.NewSiteUserGroup.as_view(), name='new_group'),
    path('group-detail/<int:pk>/', views.GroupDetail.as_view(), name='group_detail'),
]

urlpatterns += [
    path('new-api-key/', views.get_api_key, name='new_api_key'),
    path('reset-api-key/', views.reset_api_key, name='reset_api_key'),
]

urlpatterns += [
    path('manage-account/', views.account_management, name='account_management'),
    path('set-social-password/', views.social_password, name='social_password'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('siteuser:password_change_done')), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('siteuser:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('siteuser:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
