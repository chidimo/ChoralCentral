"""run fixtures/song_from_file.py"""

import json
from random import choice, randint

from setupshell import setupshell

from author.models import Author
from siteuser.models import SiteUser
from song.models import Song
from language.models import Language
from voicing.models import Voicing

from seed import SCRIPTURE

USERS = SiteUser.objects.all()

def create_songs(file_name):
    with open(file_name, "r+") as rh:
        SONG_FILE = json.load(rh)

    for song in SONG_FILE:

        authors = []

        for name, about in song["author"].items():
            names = name.rsplit(" ")

            try:
                first_name=names[0]
                last_name=names[1]
            except IndexError:
                first_name = last_name = "Unknown"

            authors.append(
                Author.objects.get_or_create(
                    originator=choice(USERS),
                    first_name=first_name,
                    last_name=last_name,
                    bio=about,
                    author_type="LYRICIST"
                    )
                )

        voicing = Voicing.objects.get(voicing="SATB")
        language = Language.objects.get(language='ENGLISH')

        song, _ = Song.objects.get_or_create(originator=choice(USERS),
                                          title=song.get("title", "None"),
                                          status="PUBLISHED",
                                          lyrics=song.get("lyrics", "None"),
                                          scripture_ref=choice(SCRIPTURE),
                                          tempo=randint(45, 250),
                                          bpm=randint(4, 8),
                                          divisions=randint(4, 8),
                                          voicing=voicing,
                                          language=language)
        for author, _ in authors:
            song.authors.add(author)

def add_manyfields():
    for each in Song.objects.all():
        each.seasons.add(randint(1, 3), randint(4, 7))
        each.mass_parts.add(randint(1, 5), randint(6, 10))
        each.likes.add(choice(USERS), choice(USERS), choice(USERS), choice(USERS))

if __name__ == "__main__":
    setupshell()
    create_songs("fixtures/data_hymnal.json")
    add_manyfields()
    print("Songs created")
