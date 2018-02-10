"""run fixtures/siteusers.py
from fixtures import siteusers
siteusers.create_siteusers(
"""

# pylint: disable=E1101, W0611, C0411

from random import choice
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .lorem import LoremPysum
from siteuser.models import SiteUser, Role
from .seed import ROLES

CustomUser = get_user_model()

def create_roles():
    for each in ROLES:
        _, _ = Role.objects.get_or_create(role=each)

def createsuperuser():
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

def create_siteusers():
    roles = Role.objects.all()
    n = int(input("Enter number of users to create: "))

    for _ in range(n):
        stx = LoremPysum("fixtures/eng_names.txt", "fixtures/igbo_names.txt")
        email = stx.email()
        try:
            user = CustomUser.objects.create_user(email=email)
            user.set_password("dwarfstar")
            user.is_active = True
            user.save()
        except IntegrityError:
            raise "IntegrityError"

        first_name = stx.word()
        last_name = stx.word()
        location = stx.word()
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

if __name__ == "__main__":
    pass