from .base import *
DEBUG = config('DEBUG', default=False, cast=bool)
SKIP_TASK = False # custom variable to be used to skip certain mgt tasks during testing

# force https:
SECURE_SSL_REDIRECT = True
# INSTALLED_APPS += ['raven.contrib.django.raven_compat',]
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'sql_mode' : 'traditional'},
        'NAME': 'parousia$choral',
        'USER': 'parousia',
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'parousia.mysql.pythonanywhere-services.com',
        'TEST':{
            'ENGINE': 'django.db.backends.mysql',
            'NAME':'parousia$test_db'
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
            }
        },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'choralcentral_prod.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
