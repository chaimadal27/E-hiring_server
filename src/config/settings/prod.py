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



# ##### DEBUG CONFIGURATION ###############################
DEBUG = False

# ### HOST CONFIGURATION ##############################
ALLOWED_HOSTS = [getenv('SITE_DOMAINE_NAME', '0.0.0.0')]

# ##### SECURITY CONFIGURATION ############################

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# ######### CACHE CONFIGURATION ###########################

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

MIDDLEWARE += (
    'django.middleware.gzip.GZipMiddleware',
)

with open('/app/databases/databases.json', 'r') as db_file:
    DATABASES = json.load(db_file)