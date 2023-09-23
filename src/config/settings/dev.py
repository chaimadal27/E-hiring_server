"""
Django base settings for social network project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/

For more information on production settings
https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
"""
from .base import *
from os import getenv

# ### DEBUG CONFIGURATION ###########################
DEBUG = True

# ### HOST CONFIGURATION ##############################
ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '0.0.0.0,').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('POSTGRES_DB_DEFAULT', ''),
        'USER': getenv('POSTGRES_USER', ''),
        'PASSWORD': getenv('POSTGRES_PASSWORD', ''),
        'HOST': getenv('POSTGRES_HOST', ''),
        'PORT': getenv('POSTGRES_PORT', ''),
    },
    'dev': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('POSTGRES_DB_DEV', ''),
        'USER': getenv('POSTGRES_USER', ''),
        'PASSWORD': getenv('POSTGRES_PASSWORD', ''),
        'HOST': getenv('POSTGRES_HOST', ''),
        'PORT': getenv('POSTGRES_PORT', ''),
    },
}

# LOGGING CONFIG
for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['handlers'] = ['console']

# END LOGGING CONFIG
