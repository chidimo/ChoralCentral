from .base import *
DEBUG = True

# create test database
# https://docs.djangoproject.com/en/2.0/topics/db/multi-db/
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'sql_mode' : 'traditional'},
        'NAME': 'parousia$choral',
        'USER': 'parousia',
        'PASSWORD': get_env_variable('CENTRAL_PASS'),
        'HOST': 'parousia.mysql.pythonanywhere-services.com',
        'TEST':{
            # 'ENGINE': 'django.db.backends.mysql',
            # 'NAME':'parousia$test_db'
            'ENGINE': 'django.db.backends.sqlite3', # for sqlite3
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
    'for_testing': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
