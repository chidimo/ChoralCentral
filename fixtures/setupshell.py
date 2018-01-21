"""run fixtures/setupshell.py"""

def setupshell():
    global datetime, django, randint, choice, timezone, get_user_model, slugify,\
        Author, Post, Comment, MassPart, Season, Language,\
        Request, Reply, Collection, Favorites, SiteUser, Role,\
        Song, Score, Midi, VideoLink, Voicing

    import datetime
    import django
    from random import randint, choice
    
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from django.template.defaultfilters import slugify

    from author.models import Author
    from blog.models import Post, Comment
    from masspart.models import MassPart
    from season.models import Season
    from language.models import Language
    from request.models import Request, Reply
    from social.models import Collection, Favorite
    from siteuser.models import SiteUser, Role
    from song.models import Song
    from song_media.models import Score, Midi, VideoLink
    from voicing.models import Voicing
    
    django.setup()

    CustomUser = get_user_model()

if __name__ == "__main__":
    setupshell()
