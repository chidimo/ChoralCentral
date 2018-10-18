from song.models import Song, Language,  Voicing
from siteuser.models import SiteUser, Message

def site_stats(request):
    return {
        'lang_count' : Language.objects.count(),
        'voice_count' : Voicing.objects.count(),
    }
