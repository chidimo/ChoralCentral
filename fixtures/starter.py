"""fixtures"""
import os
import sys
import json
from random import choice, randint

import django
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from pywebber import LoremPysum

from masspart.models import MassPart
from season.models import Season
from author.models import Author
from siteuser.models import SiteUser, Role
from song.models import Song
from song_media.models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from blog.models import Post, Comment
from request.models import Request, Reply
from language.models import Language
from voicing.models import Voicing

AUTHORS = ["LYRICIST", "COMPOSER"]
LANGUAGE = ["english", "igbo", "bini", "ibibio", "hausa", "chinese", "yoruba"]
VOICING = ["SATB", "SSAB", "SAB", "SSABTT", "ATB", "SATTB"]
SCRIPTURE = ["Psalm 91", "Proverbs 23", "Matthew 11"]

PARTS = ["ENTRANCE", "KYRIE", "GLORIA", "ACCLAMATION", "OFFERTORY",
         "COMMUNION", "SANCTUS", "AGNUS DEI", "RECESSION", "GENERAL",
         "CAROL", "NA"]

SEASONS = ["ORDINARY TIME", "ADVENT", "CHRISTMAS", "LENT",
           "EASTER", "PENTECOST", "OTHER", "NA"]

NOTES = ["SOLFA", "STAFF", "OTHER", "LEAD"]

VOICE_PARTS = ['Soprano', 'Alto', 'Tenor', 'Bass']

NOTATIONS = ['Solfa', 'Staff']

ROLES = ["COMPOSER", "CHOIR MASTER", "CHOIR CONDUCTOR",
         "CHOIR CHAIRMAN", "ORGANIST", "GUITARIST", "DRUMMER",
         "MUSIC LOVER", "SOPRANO", "ALTO", "TENOR", "BASS",
         "BARITONE", "OTHER"]

django.setup()
CustomUser = get_user_model()

def clear():
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')

def independents():
    roles()
    seasons()
    massparts()
    voice_notation()
    voicing_language()

def roles():
    for each in ROLES:
        _, _ = Role.objects.get_or_create(role=each)

def voicing_language():
    users = SiteUser.objects.all()
    for each in VOICING:
        try:
            _, _ = Voicing.objects.get_or_create(originator=choice(users), voicing=each)
        except IntegrityError:
            continue

    for each in LANGUAGE:
        try:
            _, _ = Language.objects.get_or_create(originator=choice(users), language=each.upper())
        except IntegrityError:
            continue

def seasons():
    for each in SEASONS:
        Season.objects.get_or_create(season=each)

def massparts():
    for each in PARTS:
        MassPart.objects.get_or_create(part=each)

def voice_notation():
    for each in VOICE_PARTS:
        _, _ = VocalPart.objects.get_or_create(name=each.title())
    for each in NOTATIONS:
        _, _ = ScoreNotation.objects.get_or_create(name=each.title())

def superuser():
    try:
        su = CustomUser.objects.create_user(email='admin@choralcentral.net', password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
        pro = SiteUser(user=su,first_name="Chidi",
                     last_name="Orji", location="Abu Dhabi",
                     screen_name="CCAdmin")
        pro.save()

    except IntegrityError:
        su = CustomUser.objects.get(email='admin@choralcentral.net')
        print("Superuser {} already exists".format(su.email))

def members():
    roles = Role.objects.all()
    n = int(input("Enter number of users to create: "))

    for _ in range(n):
        lorem = LoremPysum("fixtures/eng_names.txt", "fixtures/igbo_names.txt")
        email = lorem.email()
        try:
            user = CustomUser.objects.create_user(email=email)
            user.set_password("dwarfstar")
            user.is_active = True
            user.save()
        except IntegrityError:
            continue

        first_name = lorem.word()
        last_name = lorem.word()
        location = lorem.word()
        screen_name = LoremPysum().word()

        try:
            pro = SiteUser(user=user, first_name=first_name,
                          last_name=last_name, location=location,
                          screen_name=screen_name)
            pro.save()
        except IntegrityError:
            print("profile name error")
            _ = CustomUser.objects.get(email=email).delete()
            continue

        try:
            role = choice(roles)
            pro.roles.add(role.pk)
        except IntegrityError:
            continue

def songs_from_file():
    users = SiteUser.objects.all()
    voices = Voicing.objects.all()
    languages = Language.objects.all()
    fn = os.path.join(settings.BASE_DIR, 'fixtures', 'data_hymnal.json')
    with open(fn, "r+") as rh:
        song_file = json.load(rh)

    for song in song_file:
        authors = []
        for name, about in song["author"].items():
            names = name.rsplit(" ")
            try:
                first_name=names[0].strip()
                last_name=names[1].strip()
            except IndexError:
                first_name = last_name = "Unknown"

            try:
                author = Author.objects.get(first_name=first_name, last_name=last_name)
            except:
                author = Author.objects.create(
                    originator=choice(users),
                    first_name=first_name,
                    last_name=last_name,
                    bio=about)

            authors.append(author)

        originator = choice(users)
        song = Song.objects.create(
            originator=originator,
            title=song.get("title", "Unknown"),
            publish=choice([True, False]),
            lyrics=song.get("lyrics", "No lyrics"),
            scripture_reference=choice(SCRIPTURE),
            tempo=randint(45, 250),
            bpm=randint(4, 8),
            divisions=randint(4, 8),
            voicing=choice(voices),
            language=choice(languages))

        for each in authors:
            for author, _ in authors:
                song.authors.add(author)
        song.likes.add(originator.pk)

def songs():
    users = SiteUser.objects.all()
    voices = Voicing.objects.all()
    languages = Language.objects.all()
    int(input("Enter number of songs to create: "))

    for _ in range(numb):
        lorem = LoremPysum()

        voicing = Voicing.objects.get(voicing=choice(VOICING))
        language = Language.objects.get(language=choice(LANGUAGE).upper())

        _ = Song.objects.create(
            originator=choice(users),
            title=lorem.title(),
            publish=choice([True, False]),
            lyrics=lorem.paragraphs(count=randint(2, 4)),
            first_line=lorem.sentence()[:50],
            scripture_reference=choice(SCRIPTURE),
            tempo=randint(45, 250),
            bpm=randint(4, 8),
            divisions=randint(4, 8),
            voicing=choice(voices),
            language=choice(languages))

def add_manyfields():
    users = SiteUser.objects.all()
    for each in Song.objects.all():
        each.seasons.add(randint(1, 3), randint(4, 7))
        each.mass_parts.add(randint(1, 5), randint(6, 10))
        each.likes.add(choice(users), choice(users), choice(users), choice(users))
        aut = len(Author.objects.all())
        if not each.authors:
            each.authors.add(randint(1, aut-1), randint(1, aut-1))

def requests():
    numb = int(input("Enter number of requests to create "))
    users = SiteUser.objects.all()
    lorem = LoremPysum()
    for _ in range(numb):
        _ = Request.objects.create(
            originator=choice(users),
            request=lorem.title(),
            status=choice([True, False]))

def replies():
    songs = Song.objects.all()
    users = SiteUser.objects.all()
    requests = Request.objects.all()

    for request in requests[:len(requests)//2]:
        # if request.status == ""
        try:
            Reply.objects.get_or_create(
                originator=choice(users),
                request=request,
                song=choice(songs))
        except (IntegrityError, IndexError):
            continue

def authors():
    numb = int(input("Enter number of authors to create "))
    users = SiteUser.objects.all()
    for _ in range(numb):
        lorem = LoremPysum()
        _, _ = Author.objects.get_or_create(
            originator=choice(users),
            first_name=lorem.word(),
            last_name=lorem.word(),
            bio=lorem.paragraphs(count=randint(1, 3)),
            author_type=choice(AUTHORS))

def posts():
    users = SiteUser.objects.all()
    SONGS = Song.objects.all()
    lorem = LoremPysum()
    numb = int(input("Enter number of posts to create "))

    for _ in range(numb):
        title = lorem.title()
        body = lorem.sentences(count=randint(4, 8))

        selector = randint(0, 1)
        if selector and (len(SONGS) > 0):
            _ = Post.objects.get_or_create(
                    creator=choice(users),
                    title=title,
                    body=body,
                    song=choice(SONGS),
                    publish=choice([True, False]))
        else:
            _ = Post.objects.get_or_create(
                    creator=choice(users),
                    title=title,
                    body=body,
                    publish=choice([True, False]))

def comments():
    users = SiteUser.objects.all()
    lorem = LoremPysum()

    for post in Post.objects.all():
        for _ in range(randint(5, 50)):
            _ = Comment.objects.create(
                creator=choice(users),
                post=post,
                comment=lorem.sentence())

if __name__ == "__main__":
    pass
