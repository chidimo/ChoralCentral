from song.models import Song, Language,  Voicing
from siteuser.models import SiteUser, Message

def site_stats(request):
    return {
        'lang_count' : Language.objects.count(),
        'voice_count' : Voicing.objects.count(),
        'song_count' : Song.objects.filter(publish=True).count(),
    }

def unread_messages(request):
    try:
        unread = Message.objects.filter(receiver__user=request.user).filter(read=False).count()
        return {'unread' : unread}
    except TypeError:
        return dict()
