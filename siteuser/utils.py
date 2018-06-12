# source: https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html

import os
from django.template.defaultfilters import slugify

from functools import wraps

from django.conf import settings
from django.contrib import messages

import requests

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def save_avatar(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{}{}".format(instance.screen_name.lower(), ext)

def badge_icon(instance, filename):
    _, ext = os.path.splitext(filename)
    return "badges/{}_{}{}".format(instance.hierarchy, instance.name.lower(), ext)
