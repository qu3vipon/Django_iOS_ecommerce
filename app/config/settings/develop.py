from config.settings._base import *

DEBUG = True
INSTALLED_APPS += [
    'django_extensions'
]
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'config.wsgi.develop.application'
