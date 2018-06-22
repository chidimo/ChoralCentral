"""fixtures"""
import os
import sys
import glob
import json
from random import choice, randint

import django
from django.conf import settings
from django.db import IntegrityError
from django.core.files import File
from django.contrib.auth import get_user_model

from pywebber import LoremPysum

from author.models import Author
from siteuser.models import SiteUser, Role
from song.models import Voicing, Language, Season, MassPart, Song
from song.forms import GENRES, OCASSIONS
from song_media.models import VocalPart, ScoreNotation, Score, Midi, VideoLink
from blog.models import Post, Comment
from request.models import Request, Reply

AVATAR_PATH = os.path.join(settings.BASE_DIR, 'fixtures/wallpaper/')
IMAGES = [os.path.abspath(each) for each in glob.glob("{}/*.jpg".format(AVATAR_PATH))]
AUTHORS = ["lyricist", "composer", 'lyricist and composer']
LANGUAGE = ["english", "igbo", "bini", "ibibio", "hausa", "chinese", "yoruba", "latin", "french"]
VOICING = ["solo", "satb", "ssab", "sab", "ssabtt", "atb", "sattb"]
SCRIPTURE = ["Psalm 91", "Proverbs 23", "Matthew 11"]
LOCATIONS = ['lagos', 'abuja', 'benin', 'benin city', 'abu dhabi', 'dubai']
NOTES = ["solfa", "staff", "other", "lead"]
VOICE_PARTS = ['soprano', 'alto', 'tenor', 'bass']
NOTATIONS = ['solfa', 'staff', 'solfa + staff']

SEASONS = ["ordinary time", "advent", "christmas", "lent", "easter", "pentecost", "any", "na"]
PARTS = ["entrance", "kyrie", "gloria", "acclammation", "offertory", "communion", "sanctus",
    "agnus dei", "recession", "general", "na"]

# role number 1 is default for all users
ROLES = ['enthusiast', 'composer', 'choir master', 'conductor', 'organist', 'guitarist', 'drummer',
    'soprano', 'alto', 'tenor', 'bass', 'baritone', 'other', 'na']

django.setup()
CustomUser = get_user_model()

def roles():
    for each in ROLES:
        Role.objects.get_or_create(name=each)

def voicing_language():
    for each in VOICING:
        Voicing.objects.get_or_create(name=each)
    for each in LANGUAGE:
        Language.objects.get_or_create(name=each)

def seasons_massparts():
    for each in SEASONS:
        Season.objects.get_or_create(name=each)
    for each in PARTS:
        MassPart.objects.get_or_create(name=each)

def voice_notation():
    for each in VOICE_PARTS:
       VocalPart.objects.get_or_create(name=each)
    for each in NOTATIONS:
        ScoreNotation.objects.get_or_create(name=each)

def default_user():
    try:
        su = CustomUser.objects.create_user(email='unknown@user.net', password='unknownuser')
        su.is_active = False
        su.save()
    except IntegrityError:
        su = CustomUser.objects.get(email='default@user.net')
    try:
        SiteUser.objects.create(user=su, screen_name="Unknown-User", first_name="Unknown", last_name="User")
    except IntegrityError:
        pass

def my_account():
    try:
        su = CustomUser.objects.create_user(email='orjichidi95@gmail.com', password='dwarfstar')
        su.is_active = True
        su.save()
    except IntegrityError:
        su = CustomUser.objects.get(email='orjichidi95@gmail.com')
    try:
        SiteUser.objects.create(user=su, screen_name="parousia", first_name="Chidi", last_name="Orji", location="Abu Dhabi")
    except IntegrityError:
        pass

def superuser():
    try:
        su = CustomUser.objects.create_user(email='admin@choralcentral.net', password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
    except IntegrityError:
        su = CustomUser.objects.get(email='admin@choralcentral.net')
        pass

def members():
    roles = Role.objects.all()
    n = int(input("Enter number of users to create: "))

    for _ in range(n):
        lorem = LoremPysum("fixtures/eng_names.txt", "fixtures/igbo_names.txt")
        email = lorem.email()+str(n)
        try:
            user = CustomUser.objects.create_user(email=email)
            user.set_password("dwarfstar")
            user.is_active = True
            user.save()

            first_name = lorem.word()
            last_name = lorem.word()
            location = choice(LOCATIONS)
            screen_name = LoremPysum().word()
            try:
                member = SiteUser.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    location=location,
                    screen_name=screen_name,
                    avatar=File(open(choice(IMAGES), "rb")),
                    )
            except IntegrityError:
                member = SiteUser.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    location=location,
                    screen_name=screen_name+str(n),
                    avatar=File(open(choice(IMAGES), "rb")),
                    )
        except IntegrityError:
            continue
        try:
            role = choice(roles)
            member.roles.add(role.pk)
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
                author = Author.objects.create(creator=choice(users), first_name=first_name, last_name=last_name, author_type=choice(AUTHORS), bio=about)
            authors.append(author)

        creator = choice(users)
        title = song.get("title", "Unknown").strip()

        try:
            song = Song.objects.get(title=title)
        except:
            song = Song.objects.create(creator=creator, title=title, publish=choice([True, False]), genre=choice(GENRES),
                ocassion=choice(OCASSIONS), lyrics=song.get("lyrics", "No lyrics"), scripture_reference=choice(SCRIPTURE),
                tempo=randint(45, 250), bpm=randint(4, 8), divisions=randint(4, 8), voicing=choice(voices), language=choice(languages),
                like_count=randint(1, 100))
        for each in authors:
            song.authors.add(author)
    add_manyfields()

def songs():
    users = SiteUser.objects.all()
    voices = Voicing.objects.all()
    languages = Language.objects.all()
    numb = int(input("Enter number of songs to create: "))

    for _ in range(numb):
        lorem = LoremPysum()

        voicing = Voicing.objects.get(name=choice(VOICING))
        language = Language.objects.get(name=choice(LANGUAGE))

        _ = Song.objects.create(
            creator=choice(users),
            title=lorem.title(),
            publish=choice([True, False]),
            lyrics=lorem.paragraphs(count=randint(2, 4)),
            scripture_reference=choice(SCRIPTURE),
            tempo=randint(45, 250),
            bpm=randint(4, 8),
            divisions=randint(4, 8),
            voicing=choice(voices),
            language=choice(languages))

def add_manyfields():
    users = SiteUser.objects.all()
    for song in Song.objects.all():
        song.seasons.add(randint(1, 3), randint(4, 7))
        song.mass_parts.add(randint(1, 5), randint(6, 10))
        song.save()
        aut = len(Author.objects.all())
        if not song.authors:
            song.authors.add(randint(1, aut-1), randint(1, aut-1))

def requests():
    numb = int(input("Enter number of requests to create "))
    users = SiteUser.objects.all()
    lorem = LoremPysum()
    for _ in range(numb):
        _ = Request.objects.create(
            creator=choice(users),
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
                creator=choice(users),
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
            creator=choice(users),
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

def production_setup():
    roles()
    seasons_massparts()
    voice_notation()
    voicing_language()
    default_user()
    superuser()
    my_account()

def independents():
    roles()
    seasons_massparts()
    voice_notation()
    voicing_language()

def run_all():
    independents()
    superuser()
    members()

if __name__ == "__main__":
    pass

