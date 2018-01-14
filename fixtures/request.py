"""run fixtures/request.py"""

from random import choice
import django
from django.db import IntegrityError

from lorem_pysum import LoremPysum
from siteuser.models import SiteUser
from song.models import Song
from request.models import Request, Reply

django.setup()

USERS = SiteUser.objects.all()
SONGS = Song.objects.all()
TEX = LoremPysum()

def requests(numb):
    for _ in range(numb):
        _ = Request.objects.create(
            originator=choice(USERS),
            request=TEX.title(),
            status=choice(["MET", "UNMET"]))

def replies():
    requests = Request.objects.all()

    for request in requests[:len(requests)//2]:
        # if request.status == ""
        try:
            Reply.objects.get_or_create(
                originator=choice(USERS),
                request=request,
                song=choice(SONGS))
        except (IntegrityError, IndexError):
            continue        

if __name__=="__main__":
    requests(int(input("Enter number of requests to create ")))
    replies()
