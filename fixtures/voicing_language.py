"""run fixtures/voicing_language.py"""

from random import choice
from django.db import IntegrityError

from siteuser.models import SiteUser
from language.models import Language
from voicing.models import Voicing

from .setupshell import setupshell
from .seed import VOICING, LANGUAGE

USERS = SiteUser.objects.all()

def create_voicing_language():
    for each in VOICING:
        try:
            _, _ = Voicing.objects.get_or_create(originator=choice(USERS), voicing=each)
        except IntegrityError:
            continue

    for each in LANGUAGE:
        try:
            _, _ = Language.objects.get_or_create(originator=choice(USERS), language=each.upper())
        except IntegrityError:
            continue

if __name__ == "__main__":
    setupshell
    create_voicing_language()
