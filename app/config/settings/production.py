import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config.settings._base import *

DEBUG = False
INSTALLED_APPS += [
]
ALLOWED_HOSTS += [
    '.ec2-15-164-49-32.ap-northeast-2.compute.amazonaws.com',
    '15.164.49.32',
    'www.marketbroccoli.ga',
    'marketbroccoli.ga',
]
WSGI_APPLICATION = 'config.wsgi.production.application'

sentry_sdk.init(
    dsn="https://08abad9dd7bd452999fc7a3e51fbd162@sentry.io/5175837",
    integrations=[DjangoIntegration()],
    send_default_pii=True
)
