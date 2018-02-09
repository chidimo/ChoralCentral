"""run fixes/song.py"""

import json
from random import choice, randint

from py_webber import LoremPysum
from setupshell import setupshell

from author.models import Author
from siteuser.models import SiteUser
from song.models import Song
from language.models import Language
from voicing.models import Voicing

from seed import SCRIPTURE, NOTES, VOICING, LANGUAGE

USERS = SiteUser.objects.all()

def create_songs(numb):
    for _ in range(numb):
        stx = LoremPysum()

        voicing = Voicing.objects.get(voicing=choice(VOICING))
        language = Language.objects.get(language=choice(LANGUAGE).upper())

        _, _ = Song.objects.get_or_create(originator=choice(USERS),
                                          title=stx.title(),
                                          status=choice(["DRAFT", "PUBLISHED"]),
                                          lyrics=stx.paragraphs(count=randint(2, 4)),
                                          first_line=stx.sentence()[:50],
                                          scripture_ref=choice(SCRIPTURE),
                                          tempo=randint(45, 250),
                                          bpm=randint(4, 8),
                                          divisions=randint(4, 8),
                                          voicing=voicing,
                                          language=language)

def add_manyfields():
    for each in Song.objects.all():
        each.seasons.add(randint(1, 3), randint(4, 7))
        each.mass_parts.add(randint(1, 5), randint(6, 10))
        each.likes.add(choice(USERS), choice(USERS), choice(USERS), choice(USERS))
        aut = len(Author.objects.all())
        each.authors.add(randint(1, aut-1), randint(1, aut-1))

if __name__ == "__main__":
    setupshell()
    create_songs(int(input("Enter number of songs to create: ")))
    add_manyfields()
    print("Songs created")
    