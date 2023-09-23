from datetime import timedelta
from django.conf import settings
from rest_framework import HTTP_HEADER_ENCODING
from types import SimpleNamespace


AUTH_REST_SETTINGS = getattr(settings, 'AUTH_REST_JWT', dict())


DEFAULTS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'UPDATE_LAST_LOGIN': True,
    'AUTH_UNIQUE_FIELD': 'email',

    'USER_ID_CLAIM': 'identification',
    'USER_ID_FIELD': 'id',

    'USER_SERIALIZER_CLASS': None,
    'PERMISSIONS_SERIALIZER_CLASS': None,

    'DB_NAME_CLAIM': 'database_name'
}


AUTH_HEADER_TYPE_BYTES = tuple( h.encode(HTTP_HEADER_ENCODING) for h in DEFAULTS['AUTH_HEADER_TYPES'])

SETTINGS = SimpleNamespace(**{ **DEFAULTS, **AUTH_REST_SETTINGS, 'AUTH_HEADER_TYPE_BYTES': AUTH_HEADER_TYPE_BYTES })
