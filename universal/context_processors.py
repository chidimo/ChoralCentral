from song.models import Song, Language,  Voicing
from siteuser.models import SiteUser

def site_stats(request):
    return {
        'lang_count' : Language.objects.count(),
        'voice_count' : Voicing.objects.count(),
        'user_count' : SiteUser.objects.count() - 1,
        'song_count' : Song.objects.filter(publish=True).count(),
    }
