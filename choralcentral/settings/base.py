"""
Django settings for choralcentral project.
"""

import os
import pygments.formatters
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages

import raven
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
ROOT_URLCONF = 'choralcentral.urls'
SECRET_KEY = config('SECRET_KEY')
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
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = 'choralcentral@gmail.com'
DEFAULT_FROM_EMAIL = 'choralcentral@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

ALGOLIA = {
    'APPLICATION_ID': config('ALGOLIA_APPLICATION_ID'),
    'API_KEY': config('ALGOLIA_API_KEY'),
    'SEARCH_API_KEY': config('ALGOLIA_SEARCH_API_KEY'),
    'INDEX_PREFIX' : 'choralcentral'
}

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

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_TWITTER_KEY = config('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config('SOCIAL_AUTH_TWITTER_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET')

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','public_profile']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'en',
  'fields': 'id, name, email'
}

SOCIAL_AUTH_YAHOO_OAUTH2_KEY = config('SOCIAL_AUTH_YAHOO_OAUTH2_KEY')
SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = config('SOCIAL_AUTH_YAHOO_OAUTH2_SECRET')

GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY')

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES' : (
    #     'blog.api.authentication.VerifyUserIsActive',
    #  ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE' : 100,
}

# Application definition

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
    'siteuser',
    'song',
    'blog',
    'author',
    'song_media',
    'redirect301',
    'request',
    'drb',
]

THIRD_PARTY_APPS = [
    'compressor',
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

INSTALLED_APPS = PREREQ_APPS +  PROJECT_APPS + THIRD_PARTY_APPS

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOAuth2',
    'social_core.backends.yahoo.YahooOpenId',
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
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
                'universal.context_processors.unread_messages',
            ],
        },
    },
]

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

# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'siteuser.CustomUser'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_ENABLED = config('COMPRESS_ENABLED')
COMPRESS_OFFLINE = config('COMPRESS_OFFLINE')
COMPRESS_OFFLINE_MANIFEST = 'compressor_manifest.json'
COMPRESS_FILTERS = {
    'css': ['compressor.filters.css_default.CssAbsoluteFilter'], 
    'js': ['compressor.filters.jsmin.JSMinFilter']
}
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
