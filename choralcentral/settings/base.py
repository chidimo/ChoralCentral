"""
Django settings for choralcentral project.
"""

import os
import pygments.formatters
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import raven
RAVEN_CONFIG = {
    'dsn': 'https://b6ecc578313140618b41d13175ed6152:88a27d13befa4ff69cd2fcec01bd6769@sentry.io/1222272',
    # If you are using git, you can also automatically configure the release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'choralcentral.urls'
SECRET_KEY = get_env_variable("SECRET_KEY")
WSGI_APPLICATION = 'choralcentral.wsgi.application'
INTERNAL_IPS = ('127.0.0.1', 'localhost')

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('siteuser:login')
LOGOUT_URL = reverse_lazy('siteuser:logout')

PASSWORD_RESET_TIMEOUT_DAYS = 1

MESSAGE_LEVEL = 10  # DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'choralcentral@gmail.com'
DEFAULT_FROM_EMAIL = 'choralcentral@gmail.com'
EMAIL_HOST_PASSWORD = get_env_variable('DEFAULT_EMAIL_PASS')

# SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}
IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
SHELL_PLUS_POST_IMPORTS = [
    ('fixtures', '*'),
    ('fixtures'),
    ('drb_fixtures', '*'),
    ('drb_fixtures'),
    ]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '778785529263-j0gliifiledngb10gptji0514o5srjqi.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'sr9-rKSYRmdRYmLpzwslIcvf'

SOCIAL_AUTH_TWITTER_KEY = 'pEmqXP2U6w8EeblGB3Eg0SvfL'
SOCIAL_AUTH_TWITTER_SECRET = 'khl62hQETrYUgh2zB9KTx7e2SPEjra76KTI2m85V4nfYzwzBgB'

SOCIAL_AUTH_FACEBOOK_KEY = '977674249054153'
SOCIAL_AUTH_FACEBOOK_SECRET = '982efc4814c26870b5bbb382ca314432'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','public_profile']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'en',
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_YAHOO_OAUTH2_KEY = 'dj0yJmk9QUpmTEdZS2lLTmd5JmQ9WVdrOVdGZG5ZMmh1TldNbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1jYg--'
SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = 'c032d7ff2a5a1af2e7276e7a8e4b0c974321d73d'

GOOGLE_RECAPTCHA_SECRET_KEY = '6LdJMlsUAAAAAJaHzAZUJsYV2UQ1tEsGK7KNL8oX'
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES' : (
    #     'blog.api.authentication.VerifyUserIsActive',
    #  ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE' : 100,
}

# Application definition

AUTOCOMPLETE_LIGHT = [
    # Must come before contrib.admin
    'dal',
    'dal_select2',
]

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps'
]

PROJECT_APPS = [
    'author',
    'blog',
    'drb',
    'request',
    'siteuser',
    'song',
    'song_media',
]

THIRD_PARTY_APPS = [
    'likes',
    'secretballot',
    'rest_framework',
    'sorl.thumbnail',
    'social_django',
    'pure_pagination',
    'django_addanother',
    'django_extensions',
    'algoliasearch_django',
    'django_social_share',
    'raven.contrib.django.raven_compat',
    'rules.apps.AutodiscoverRulesConfig',
]

INSTALLED_APPS = AUTOCOMPLETE_LIGHT + PREREQ_APPS +  PROJECT_APPS + THIRD_PARTY_APPS

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOAuth2',
    'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
    'rules.permissions.ObjectPermissionBackend',
    )

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.user.get_username',
    'siteuser.save_social.save_social_profile', # override create_user
    'social_core.pipeline.social_auth.social_user',
    # 'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'universal.context_processors.site_stats',
            ],
        },
    },
]


ALGOLIA = {
    'APPLICATION_ID': 'UTXB87TRN7',
    'API_KEY': '3319d9c270b17c886367aaa05efe7326',
    'SEARCH_API_KEY': 'fedeb1405dc0324ff4b7378b5b930056',
    'INDEX_PREFIX' : 'choralcentral'
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'siteuser.CustomUser'
