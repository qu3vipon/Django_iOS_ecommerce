from config.settings._base import *

DEBUG = False
INSTALLED_APPS += [
]
ALLOWED_HOSTS = [
    'ec2-15-164-49-32.ap-northeast-2.compute.amazonaws.com',
]
WSGI_APPLICATION = 'config.wsgi.production.application'
