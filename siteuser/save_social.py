# from django.core.files import File
import json

import requests

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import SiteUser

CustomUser = get_user_model()

login_backends = {}
login_backends['django'] = 'django.contrib.auth.backends.ModelBackend'
login_backends['twitter'] = 'social_core.backends.twitter.TwitterOAuth'
login_backends['google_oauth2'] = 'social_core.backends.google.GoogleOAuth2'
login_backends['facebook'] = 'social_core.backends.facebook.FacebookOAuth2'
login_backends['yahoo'] = 'social_core.backends.yahoo.YahooOAuth2'

def save_avatar(image_url, model_object):
    response = requests.get(image_url)
    if response.status_code == 200:
        name = model_object.screen_name.lower()
        model_object.avatar.save(name, ContentFile(response.content), save=True)

def save_social_profile(backend, user, response, *args, **kwargs):
    request = kwargs['request']

    if backend.name == "twitter":
        # with open("response-twitter.json", "w+") as fh:
        #     json.dump(response, fh)
        screen_name = response['screen_name'] # twitter response contains a screen_name
        image = response['profile_image_url']
        location = response['location']
        name = response['name'].split()
        first_name = name[0]
        last_name = name[1]
        email = response.get('email', None)
        if email is None:
            msg = """It appears you have no email set in your twitter account.
            We have created a dummy email {} for your for purpose of registration.
            Please be sure to change it to a real email.""".format(email)
            messages.success(request, msg)

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
        else:
            user = CustomUser.objects.create_user(email=email, password=None)
            user.is_active = True
            user.save()
        try:
            su = SiteUser.objects.get(user__email=email)
        except ObjectDoesNotExist:
            su = SiteUser.objects.create(
                user=user, screen_name=screen_name, first_name=first_name, last_name=last_name,
                location=location)
            save_avatar(image, su)
        login(request, user, backend=login_backends['django'])
        return {'username' : screen_name}

    elif backend.name == 'google-oauth2':
        # with open("response-google.json", "w+") as fh:
        #     json.dump(response, fh)
        screen_name = response['displayName'].strip()
        email = response['emails'][0]['value']
        first_name = response['name']['givenName']
        last_name = response['name']['familyName']
        image = response['image']['url'].split('?')[0]

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
        else:
            user = CustomUser.objects.create_user(email=email, password=None)
            user.is_active = True
            user.save()
        try:
            su = SiteUser.objects.get(user__email=email)
        except ObjectDoesNotExist:
            su = SiteUser.objects.create(
                user=user, screen_name=screen_name, first_name=first_name, last_name=last_name)
            save_avatar(image, su)
        login(request, user, backend=login_backends['django'])
        return {'username' : screen_name}

    elif backend.name == 'facebook':
        # with open("response-facebook.json", "w+") as fh:
        #     json.dump(response, fh)
        name = response['name'].split()
        first_name = name[0]
        last_name = name[1]
        screen_name = "{}-{}".format(first_name, last_name)
        email = response.get('email', None)
        image = 'https://graph.facebook.com/{}/picture?type=large'.format(response['id'])

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
        else:
            user = CustomUser.objects.create_user(email=email, password=None)
            user.is_active = True
            user.save()
        try:
            su = SiteUser.objects.get(user__email=email)
        except ObjectDoesNotExist:
            su = SiteUser.objects.create(
                user=user, screen_name=screen_name, first_name=first_name, last_name=last_name)
            save_avatar(image, su)
        login(request, user, backend=login_backends['django'])
        return {'username' : screen_name}

    elif backend.name == 'yahoo-oauth2':
        # with open("response-yahoo.json", "w+") as fh:
        #     json.dump(response, fh)
        image = response['image']['imageUrl']
        screen_name = response['nickname'] # not unique. check for collisions

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            siteuser = SiteUser.objects.get(screen_name=screen_name)
            user = siteuser.user
            login(request, user, backend=login_backends['django'])
            return {'username' : screen_name}

        email = "ab@yahoo.com"
        user = CustomUser.objects.create_user(email=email, password=None)
        user.is_active = True
        user.save()

        su = SiteUser.objects.create(
            user=user, screen_name=screen_name, first_name='first_name', last_name='last_name')
        save_avatar(image, su)

        login(request, user, backend=login_backends['django'])
        return {'username' : screen_name}
