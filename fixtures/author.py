"""run fixtures/author.py"""

from random import choice, randint

from author.models import Author
from siteuser.models import SiteUser

from py_webber import LoremPysum

from .seed import AUTHORS



def create_authors(numb):
    USERS = SiteUser.objects.all()
    for _ in range(numb):
        stx = LoremPysum()
        _, _ = Author.objects.get_or_create(originator=choice(USERS),
                                            first_name=stx.word(),
                                            last_name=stx.word(),
                                            bio=stx.paragraphs(count=randint(1, 3)),
                                            author_type=choice(AUTHORS))


if __name__ == "__main__":
    pass
