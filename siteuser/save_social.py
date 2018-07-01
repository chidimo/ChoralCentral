# from django.core.files import File
import json
from random import randint

import requests

from django.template.defaultfilters import slugify

from django.db import IntegrityError
# from django.core.exceptions import ObjectDoesNotExist
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

def process_response(request, backend, response):
    """Process the response returned by a backend"""
    save_name = "response-{}.json".format(backend.name)
    with open(save_name, "w+") as fh:
        json.dump(response, fh)
    if backend.name == "twitter":
        screen_name = slugify(response['screen_name']) # twitter response contains a screen_name
        email = response.get('email', None)
        image = response['profile_image_url']
        location = response['location']
        first_name = response['name'].split()[0]
        try:
            last_name = response['name'].split()[1]
        except IndexError:
            last_name = ''
        if email is None:
            msg = """It appears you have no email set in your twitter account.
            We have created a dummy email {} for you for purpose of registration.
            Please be sure to change it to a real email.""".format(email)
            messages.success(request, msg)

    elif backend.name == 'google-oauth2':
        screen_name = slugify(response['displayName'].strip())
        email = response['emails'][0]['value']
        first_name = response['name']['givenName']
        last_name = response['name']['familyName']
        image = response['image']['url'].split('?')[0]
        location = "Unknown location"

    elif backend.name == 'facebook':
        first_name = response['name'].split()[0]
        try:
            last_name = response['name'].split()[1]
        except IndexError:
            last_name = ''
        screen_name = slugify("{}-{}".format(first_name, last_name))
        email = response.get('email', None)
        image = 'https://graph.facebook.com/{}/picture?type=large'.format(response['id'])
        location = "Unknown location"

    elif backend.name == 'yahoo-oauth2':
        screen_name = slugify(response['nickname']) # not unique. check for collisions
        email = "{}@yahoo.com".format(response['guid'].lower()) # make email from guid
        image = response['image']['imageUrl']
        msg = """We couldn't find your yahoo mail address so
        We have created a dummy email {} for you for purpose of registration.
        Please be sure to change it to a real email.""".format(email)
        messages.success(request, msg)
        first_name = "Unknown location"
        last_name = "Unknown location"
        location = "Unknown location"
    else:
        print("Backend not found")
        return
    return screen_name, email, image, first_name, last_name, location

def get_and_login_siteuser(request, user, screen_name, email, image, first_name, last_name, location):
    """If siteuser exists, just log it in and move on, else create it and log it in"""
    if SiteUser.objects.filter(user=user).exists():
        pass
    else:
        while True: # keep looping until a SiteUser is successfully created
            try:
                su = SiteUser.objects.create(user=user, screen_name=screen_name, first_name=first_name, last_name=last_name, location=location)
                save_avatar(image, su)
                break
            except IntegrityError:
                screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                continue
    login(request, user, backend=login_backends['django'])

def get_or_create_user_from_social_detail(request, screen_name, email, image, first_name, last_name, location):
    """Create new user from social profile details"""
    if CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.get(email=email)
    else:
        user = CustomUser.objects.create_user(email=email, password=None)
        user.is_active = True
        user.save()
    get_and_login_siteuser(request, user, screen_name, email, image, first_name, last_name, location)

def save_social_profile(backend, user, response, *args, **kwargs):
    request = kwargs['request']

    # if a user is already logged in and just wants to connect a social media account, just login the user
    if request.user.is_authenticated:
        login(request, request.user, backend=login_backends['django'])
    else:
        screen_name, email, image, first_name, last_name, location = process_response(request, backend, response)
        get_or_create_user_from_social_detail(request, screen_name, email, image, first_name, last_name, location)
