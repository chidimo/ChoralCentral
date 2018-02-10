"""choralcentral URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("$", views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("$", Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import path, include
    2. Add a URL to urlpatterns:  path("blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from blog.sitemaps import PostSiteMap
from request.sitemaps import RequestSiteMap
from siteuser.sitemaps import SiteUserSiteMap
from song.sitemaps import SongSiteMap

sitemaps = {
    "posts" : PostSiteMap,
    "requests" : RequestSiteMap,
    "siteusers" : SiteUserSiteMap,
    "songs" : SongSiteMap,
}

urlpatterns = [
    path("", include('song.urls')),
    path("admin/", admin.site.urls),
    path("author/", include('author.urls')),
    path("blog/", include('blog.urls')),
    path("language/", include('language.urls')),
    path("request/", include('request.urls')),
    path("users/", include('siteuser.urls')),
    # path("song/", include('song.urls')),
    path("song-media/", include('song_media.urls')),
    path("voicing/", include('voicing.urls')),
    path("permission-denied/", views.permission_denied, name='permission_denied'),
    # path("search/", include('haystack.urls')),
    path("accounts/", include('django.contrib.auth.urls')),
    path("sitemap\.xml/", sitemap, {'sitemaps' : sitemaps},
        name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
