from base import *
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

DEBUG = False

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {'sql_mode' : 'traditional'},
    'NAME': 'sohtire$choralcentral',
    'USER': 'sohtire',
    'PASSWORD': get_env_variable('CENTRAL_PASS'),
    'HOST': 'parousia.mysql.pythonanywhere-services.com',
    'TEST':{
        # 'ENGINE': 'django.db.backends.sqlite3', # for sqlite3
        # 'NAME':'test.db',
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'parousia$test_default'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# heroku specific settings
import django_heroku
django_heroku.settings(locals())
