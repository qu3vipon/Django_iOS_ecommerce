from config.settings._base import *

DEBUG = True
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]
ALLOWED_HOSTS += [
    '*',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
WSGI_APPLICATION = 'config.wsgi.develop.application'
INTERNAL_IPS = [
    '127.0.0.1',
]
