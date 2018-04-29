from song.models import Song, Language
from siteuser.models import SiteUser

def site_stats(request):
    return {
        'lang_count' : Language.objects.count(),
        'user_count' : SiteUser.objects.count() - 1,
        'song_count' : Song.objects.count(),
    }