"""run fixtures/siteusers.py"""

# pylint: disable=E1101, W0611, C0411

import django
from random import randint, choice
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from setupshell import setupshell

from lorem_pysum import LoremPysum
from siteuser.models import SiteUser, Role
from seed import ROLES

CustomUser = get_user_model()

def create_roles():
    for each in ROLES:
        _, _ = Role.objects.get_or_create(role=each)

def createsuperuser():
    try:
        su = CustomUser.objects.create_user(email='admin@somto.com', password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
        pro = SiteUser(user=su,first_name="somto",
                     last_name="chukwu", location="somewhere",
                     screen_name="Somto")
        pro.save()

    except IntegrityError:
        su = CustomUser.objects.get(email='admin@somto.com')
        print("Superuser {} already exists".format(su.email))

def create_siteusers(n):
    num_roles = len(Role.objects.all())

    for _ in range(n):
        stx = LoremPysum("fixtures/eng_names.txt", "fixtures/igbo_names.txt", lorem=False)
        email = "{}@{}.{}".format(stx.word(), stx.word(), choice(["com", "org", "info"]))
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

        for i in range(randint(1, num_roles-10)):
            try:
                pro.roles.add(i)
            except IntegrityError:
                continue

if __name__ == "__main__":
    setupshell()
    createsuperuser()
    create_roles()
    create_siteusers(int(input("Enter number of users to create: ")))
    print("SiteUsers created successfully")
