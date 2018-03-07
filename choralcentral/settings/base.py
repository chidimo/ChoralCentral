"""
Django settings for choralcentral project.
"""

import os
import pygments.formatters
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

FIXTURE_DIRS = [os.path.join(BASE_DIR, "fixtures")]

SITE_ID = 1

LOGIN_REDIRECT_URL = reverse_lazy('song:index')
LOGIN_URL = reverse_lazy('siteuser:login')
LOGOUT_URL = reverse_lazy('siteuser:logout')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'choralcentral@gmail.com'
DEFAULT_FROM_EMAIL = 'choralcentral@gmail.com'
EMAIL_HOST_PASSWORD = get_env_variable('DEFAULT_EMAIL_PASS')

SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}
IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
SHELL_PLUS_POST_IMPORTS = [
    ('fixtures', '*'),
    ('fixtures')
    ]

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
    'author',
    'blog',
    'masspart',
    'season',
    'language',
    'request',
    'siteuser',
    'song',
    'song_media',
    'voicing',
]

THIRD_PARTY_APPS = [
    'guardian',
    # 'hitcount',
    'sorl.thumbnail',
    'social_django',
    'pure_pagination',
    'django_addanother',
    'django_extensions',
    'algoliasearch_django',
]

INSTALLED_APPS = PREREQ_APPS +  PROJECT_APPS + THIRD_PARTY_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # guardian backend
    'guardian.backends.ObjectPermissionBackend',
    # social backends
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.yahoo.YahooOpenId',
    # 'social.backends.facebook.FacebookOAuth2',

    )

GUARDIAN_RENDER_403 = True
# GUARDIAN_TEMPLATE_403 = "403.html"

# social-auth namespace setting. Override setting in project.urls
# SOCIAL_AUTH_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_FACEBOOK_KEY =   # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET =   # App Secret


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
