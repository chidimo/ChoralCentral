"""run fixtures/author.py"""

from random import choice, randint

from author.models import Author
from siteuser.models import SiteUser

from lorem_pysum import LoremPysum
from seed import AUTHORS
from setupshell import setupshell

USERS = SiteUser.objects.all()

def create_authors(numb):
    for _ in range(numb):
        stx = LoremPysum()
        _, _ = Author.objects.get_or_create(originator=choice(USERS),
                                            first_name=stx.word(),
                                            last_name=stx.word(),
                                            bio=stx.paragraphs(count=randint(1, 3)),
                                            author_type=choice(AUTHORS))
                                            

        # for each in SONG_FILE:
        #     author = each["author"].lsplit(" ")
        #     first_name = author[0]
        #     last_name = author[1]
        #     bio = each["about"]

        #     Author.objects.get_or_create(
        #         originator=choice(USERS),
        #         first_name=first_name,
        #         last_name=last_name ,
        #         bio=bio,
        #         author_type=choice(["LYRICIST", "COMPOSER"])
        #     )

if __name__ == "__main__":
    setupshell()
    create_authors(int(input("Enter number of authors to create: ")))
    print("Authors created")
    