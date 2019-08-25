# http://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
# http://www.django-rest-framework.org/api-guide/authentication/#django-oauth-toolkit
# https://stackoverflow.com/questions/32844784/django-rest-framework-custom-authentication#32846841

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate as django_authenticate
from rest_framework import authentication, exceptions

class VerifyUserIsActive(authentication.BaseAuthentication):
    def authenticate(self, request):

        # Get the username and password
        username = request.data['username']
        password = request.data['password']
        print('USERNAME', username)
        print('PASSWORD', password)

        if not username or not password:
            raise exceptions.AuthenticationFailed("No credentials provided. You're probably logged out. Please login to continue.")

        credentials = {
            get_user_model().USERNAME_FIELD: username,
            'password': password
        }

        user = django_authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)  # authentication successful
