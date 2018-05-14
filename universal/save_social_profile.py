# from django.core.files import File
# import json
from urllib.request import urlopen
from io import BytesIO

from django.core.files import File
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from siteuser.models import SiteUser

CustomUser = get_user_model()

def download_avatar(url):
    r = urlopen(url)
    return BytesIO(r.read())

def save_social_profile(backend, user, response, *args, **kwargs):
    request = kwargs['request']
    login_backend = 'django.contrib.auth.backends.ModelBackend',
    if backend.name == "twitter":
        # with open("res.json", "w+") as fh:
        #     json.dump(response, fh)

        login_backend = 'social_core.backends.twitter.TwitterOAuth'
        screen_name = response['screen_name'] # twitter response contains a screen_name
        image = response['profile_image_url']
        location = response['location']
        name = response['name'].split()
        first_name = name[0]
        last_name = name[1]
        email = "{}@twitter.com".format(screen_name) # make a fake email to satisfy create_user

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            siteuser = SiteUser.objects.get(screen_name=screen_name)
            user = siteuser.user
            login(request, user, backend=login_backend)
            return {'username' : screen_name}

        user = CustomUser.objects.create_user(email=email, password=None)
        user.is_active = True
        user.save()

        su = SiteUser.objects.create(
            user=user, screen_name=screen_name, first_name=first_name, last_name=last_name,
            location=location)
        su.avatar = File(download_avatar(image))
        su.save()

        login(request, user, backend=login_backend)
        return {'username' : screen_name}

    elif backend.name == 'google-oauth2':
        # with open("google-res.json", "w+") as fh:
        #     json.dump(response, fh)

        login_backend = 'social_core.backends.google.GoogleOAuth2'
        screen_name = response['displayName'].strip()
        email = response['emails'][0]['value']
        first_name = response['name']['givenName']
        last_name = response['name']['familyName']
        image = response['image']['url'].split('?')[0]

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            siteuser = SiteUser.objects.get(screen_name=screen_name)
            user = siteuser.user
            login(request, user, backend=login_backend)
            return {'username' : screen_name}

        user = CustomUser.objects.create_user(email=email, password=None)
        user.is_active = True
        user.save()

        su = SiteUser.objects.create(
            user=user, screen_name=screen_name, first_name=first_name, last_name=last_name)
        su.avatar = File(download_avatar(image))
        su.save()


        login(request, user, backend=login_backend)
        return {'username' : screen_name}

    elif backend.name == 'facebook':
        pass

