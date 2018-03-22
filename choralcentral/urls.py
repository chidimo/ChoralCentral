"""urls"""
from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from blog.sitemaps import PostSiteMap
from request.sitemaps import RequestSiteMap
from siteuser.sitemaps import SiteUserSiteMap
from song.sitemaps import SongSiteMap

from blog.api.urls import blog_api_urls
from siteuser.api.urls import user_api_urls
from song.api.urls import song_api_urls

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
    path("request/", include('request.urls')),
    path("users/", include('siteuser.urls')),
    path("song-media/", include('song_media.urls')),
    # path("permission-denied/", views.permission_denied, name='permission_denied'),
    path('social/', include('social_django.urls', namespace='social')),
    path("sitemap\.xml/", sitemap, {'sitemaps' : sitemaps},
        name="django.contrib.sitemaps.views.sitemap"),

    # path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-blog/', include((blog_api_urls, 'blog-api'))),
    path('api-users/', include((user_api_urls, 'user-api'))),
    path('api-songs/', include((song_api_urls, 'song-api'))),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
