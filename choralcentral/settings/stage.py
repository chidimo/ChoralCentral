from .base import *
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

DEBUG = False

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {'sql_mode' : 'traditional'},
    'NAME': 'choralcentral$choral',
    'USER': 'choralcentral',
    'PASSWORD': get_env_variable('CENTRAL_PASS'),
    'HOST': 'choralcentral.mysql.pythonanywhere-services.com',
    'TEST':{
        # 'ENGINE': 'django.db.backends.sqlite3', # for sqlite3
        # 'NAME':'test.db',
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'choralcentral$test_db'
        }
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
            'filename': os.path.join(BASE_DIR, 'choralcentral_stage.log'),
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

# heroku specific settings
import django_heroku
django_heroku.settings(locals())
