"""run fixtures/song_from_file.py

create_songs("fixtures/data_hymnal.json")
"""

import json
from random import choice, randint

from author.models import Author
from siteuser.models import SiteUser
from song.models import Song
from language.models import Language
from voicing.models import Voicing

from .seed import SCRIPTURE

def create_songs_from_file(file_name):
    USERS = SiteUser.objects.all()
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
                    )
                )
        originator = choice(USERS)
        voicing = Voicing.objects.get_or_create(voicing="SATB")[0]
        language = Language.objects.get_or_create(language='ENGLISH')[0]

        song, _ = Song.objects.get_or_create(originator=originator,
                                          title=song.get("title", "None"),
                                          status="PUBLISHED",
                                          lyrics=song.get("lyrics", "None"),
                                          scripture_ref=choice(SCRIPTURE),
                                          tempo=randint(45, 250),
                                          bpm=randint(4, 8),
                                          divisions=randint(4, 8),
                                          voicing=voicing,
                                          language=language)
        for each in authors:
            for author, _ in authors:
                song.authors.add(author)
        song.likes.add(originator.pk)

def add_manyfields():
    USERS = SiteUser.objects.all()
    for each in Song.objects.all():
        each.seasons.add(randint(1, 3), randint(4, 7))
        each.mass_parts.add(randint(1, 5), randint(6, 10))
        each.likes.add(choice(USERS), choice(USERS), choice(USERS), choice(USERS))

if __name__ == "__main__":
    pass
