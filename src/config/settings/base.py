# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJkYXRhYmFzZV9uYW1lIjoiZGV2In0.6jCS1LvQUX3fuAqI0uIYswsdUhZ7jWC3NrpkQBClgi4

"""
Django settings for LPRS_Core project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from os import listdir, getenv
from os.path import basename, dirname, join, normpath, abspath
from sys import path
from datetime import timedelta

# ### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
PROJECT_NAME = basename(DJANGO_ROOT)

# Project domain:
# PROJECT_DOMAIN = '%s.com' % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(PROJECT_ROOT)

# add apps/ to the Python path
path.append(normpath(join(PROJECT_ROOT, 'apps')))

# collect media files here
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

# ##### SECURITY CONFIGURATION ############################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', '2276i2-j5%_*c#tto+-95n$8sw94e5gf8efi$hzsisvt5c4aqo')

# auth groups config
SECURITY_DIR = normpath(join(PROJECT_ROOT, 'security'))

# ##### APPLICATION CONFIGURATION #########################

# Application definition

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
# APP CONFIGURATION
INSTALLED_APPS = (
    # Defaul Django apps

    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg2',

    # e hiring apps
    'apps.core',
    'apps.jwt_authentication',
    'apps.user_managment',
    'apps.referentiel_managment',
    'apps.lists_managment',
    'apps.candidate_managment',
    'apps.offer_managment',


    # timetracking apps
    
    'apps.legal_agency',
    'apps.resource_state',
    'apps.social_networks',
    'apps.timesheet',
    'apps.resource_advantages',
    'apps.global_settings',
    

)

# middleware configuration
MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.jwt_authentication.middleware.MultiDBMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_EXPOSE_HEADERS = (
    'Content-Disposition',
)

SESSION_ENGINE = "django.contrib.sessions.backends.file"

# fixture configuration
# https://docs.djangoproject.com/fr/2.2/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    normpath(join(PROJECT_ROOT, 'fixtures')),
)

# template configuration
TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(PROJECT_ROOT, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
)

# rest_framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.jwt_authentication.authentication.CustomJWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'apps.core.exception_handler.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.CustomPagination',
    'DATETIME_FORMAT': "%d/%m/%Y %H:%M:%S",
    'DATE_FORMAT': "%d/%m/%Y",
    "DATE_INPUT_FORMATS": ["%d/%m/%Y"],
}
SUPER_ADMIN_GROUP = 'Super Admin'
ADMINISTRATION_GROUP_NAME = 'Administration'
DIRECTION_GROUP_NAME = 'Direction'
RRH_GROUP_NAME = 'RRH'
OPERATIONNEL_GROUP_NAME = 'Opérationnel'
SOURCEUR_GROUP_NAME = 'Sourceur'

IMMUTABLE_GROUPS = (
    {
        'name':SUPER_ADMIN_GROUP, 'permissions':[
            'view_legalagency',
            'add_legalagency',
            'change_legalagency',
            'activate_legalagency',
            'delete_legalagency',
    ]},
    {'name': ADMINISTRATION_GROUP_NAME, 'permissions': [
        # permissions
    ]},
    {'name': DIRECTION_GROUP_NAME, 'permissions': [
        # permissions
    ]},
    {'name': RRH_GROUP_NAME, 'permissions': [
        # permissions
    ]},
    {'name': OPERATIONNEL_GROUP_NAME, 'permissions': [
        # permissions
    ]},
    {'name': SOURCEUR_GROUP_NAME, 'permissions': [
        # permissions
    ]},
)
# BEGIN ACTIVITY TYPE MANAGMENT
PRODUCTION = 'Production'
WORK_ON_REMOTE = 'En ligne'
PAID_LEAVE = 'Congé'
SICK_LEAVE = 'Congé de maladie'

ACTIVITY_TYPE = (
        {'activity_type_name':PRODUCTION},
        {'activity_type_name':PAID_LEAVE},
        {'activity_type_name':SICK_LEAVE}
        )
# END ACTIVITY TYPE MANAGMENT

# BEGIN ACTIVITY MANAGMENT

PROD_T1 = 'Recrutement'
PROD_T2 = 'Test'

ACTIVITY = (
        {'activity_name':PROD_T1,'activity_type':PRODUCTION},
        )

# END ACTIVITY MANAGMENT




# BEGIN LISTS MANAGMENT

DISPONIBILITY_LIST_NAME='Disponibilité'
FAMILY_SITUATION_LIST_NAME='Situation familiale'
SPECIALITY_LIST_NAME='Spécialité'
SENIORITY_LIST_NAME='Séniorité'
DEVISE_LIST_NAME='Devise'
LANGUAGE_LEVEL_LIST_NAME='Niveau langue'
TREATMENT_STATUS_LIST_NAME='Statut candidat'
LANGUAGE_LIST_NAME='Langues'
CONTRACT_TYPE_LIST_NAME='Type de contrat'
MOBILITY_LIST_NAME='Mobilité'
SOURCE_LIST_NAME='Source'
STAFF_LIST_NAME='Staff'
EDUCATION_LEVEL_LIST_NAME='Niveau d\'études'
CIVILITY_LIST_NAME='Civilité'
FUNCTION_LIST_NAME='Fonction'
COMPANY_ACTIVITY_LIST_NAME='Activity entreprise'
SCHOOL_TYPE_LIST_NAME='Type de l\'école'
IMMUTABLE_LISTS = (
    {'name': DISPONIBILITY_LIST_NAME},
    {'name':FAMILY_SITUATION_LIST_NAME },
    {'name': SPECIALITY_LIST_NAME},
    {'name': SENIORITY_LIST_NAME},
    {'name':DEVISE_LIST_NAME },
    {'name':LANGUAGE_LEVEL_LIST_NAME },
    {'name':TREATMENT_STATUS_LIST_NAME },
    {'name':LANGUAGE_LIST_NAME },
    {'name': CONTRACT_TYPE_LIST_NAME},
    {'name': MOBILITY_LIST_NAME},
    {'name': SOURCE_LIST_NAME},
    {'name':STAFF_LIST_NAME },
    {'name': EDUCATION_LEVEL_LIST_NAME},
    {'name': CIVILITY_LIST_NAME},
    {'name': COMPANY_ACTIVITY_LIST_NAME},
    {'name': SCHOOL_TYPE_LIST_NAME},
    {'name': FUNCTION_LIST_NAME},
)
# END LISTS MANAGMENT


# BEGIN JOB STATUS CONFIG
NEW_STATUS=1
VALID_STATUS=2
REJECT_STATUS=3

JOB_STATUS=(
(NEW_STATUS,"New"),
(VALID_STATUS,"Valid"),
(REJECT_STATUS,"Reject"))
#END JOB STATUS CONFIG

# BEGIN STAGE KANBAN CONFIG
TO_SORT_STAGE = 1
TO_CALL_STAGE = 2
INTERVIEW_RH_STAGE = 3
INTERVIEW_OPERATIONAL_STAGE = 4
ACCEPTED_STAGE = 5

STAGE_CANDIDATE=(
(TO_SORT_STAGE,"a trier"),
(TO_CALL_STAGE,"a appeler"),
(INTERVIEW_RH_STAGE,"entretien rh"),
(INTERVIEW_OPERATIONAL_STAGE,"entretien operationnel"),
(ACCEPTED_STAGE,"retenu"))
#END STAGE KANBAN CONFIG

# BEGIN STATUS CANDIDATE CONFIG
NEW_STATUS = 1
VIVIER_STATUS = 2


STATUS_CANDIDATE=(
(NEW_STATUS,"nouveau"),
(VIVIER_STATUS,"vivier"))

#END STATUS CANDIDATE CONFIG

# BEGIN STATUS OFFER CONFIG
NEW_STATUS=1
IN_PROCESSING_STATUS=2
CLOSE_STATUS = 3


OFFER_STATUS=(
(NEW_STATUS,"new"),
(IN_PROCESSING_STATUS,"en traitement"),
(CLOSE_STATUS,"cloturer"))

#END STATUS OFFER CONFIG

#BEGIN EXPORT CONFIG
PARTENAR_FIELD_CONFIG_CSV = ['name_fr',
                            'name_ar',
                            'telephone',
                            'email',
                            'web_site',
                            'get_activity',
                            'address_ar',
                            'address_fr',
                            'get_staff',
                            'get_responsable',
                            'get_responsable__telephone',]

PARTENAR_TITLE_CONFIG_CSV = ['Nom Entreprise fr',
                             'Nom Entreprise ar',
                             'Téléphone',
                             'Email',
                             'Site Web',
                             'Activité',
                             'Adresse fr',
                             'Adresse ar',
                             'Staff',
                             'Responsable',
                             'Téléphone Responsable',]

SCHOOL_FIELD_CONFIG_CSV = ['short_name_fr',
            'long_name_fr',
            'short_name_ar',
            'long_name_ar',
            'web_site',
            'get_type',
            'country',]

SCHOOL_TITLE_CONFIG_CSV = ['Nom Court fr',
                             'Nom Long fr',
                             'Nom Court ar',
                             'Nom Long ar',
                             'Site Web',
                             'Type',
                             'Pays',]

JOB_FIELD_CONFIG_CSV = ['name_fr','description_fr','name_fr','description_ar']

JOB_TITLE_CONFIG_CSV = ['categorie fr','description_fr','categorie ar','description_ar']

LEGAL_AGENCY_FIELD_CONFIG_CSV = [
    'agency_name',
    'agency_email',
    'agency_address',
    'agency_postal_code',
    'agency_city',
    'agency_country',
    'agency_legal_status',
    'load_factor',
    'load_rate'
]

LEGAL_AGENCY_TITLE_CONFIG_CSV = [
    'Nom agence juridique',
    'Email agence juridique',
    'Adresse agence juridique',
    'Ville agence juridique',
    'Pays agence juridique',
    'Status juridique',
    'Facteur de charge',
    'Taux de charge'
]






#END EXPORT CONFIG




SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# simple_jwt configuration
AUTH_REST_JWT = {
    # object which specifies how long access tokens are valid.
    # This timedelta value is added to the current UTC time during token
    # generation to obtain the token's default "exp" claim value.
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'RESET_PASSWORD_LINK': getenv('RESET_PASSWORD_LINK', ""),

    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'USER_SERIALIZER_CLASS': 'apps.core.serializers.UserSerializer',
    'PERMISSIONS_SERIALIZER_CLASS': 'apps.core.serializers.PermissionSerializer',
}

# internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ### DJANGO RUNNING CONFIGURATION ######################

# user model configuration
AUTH_USER_MODEL = 'core_apps.User'

# backend auth
AUTHENTICATION_BACKENDS = (
    'apps.jwt_authentication.backends.CustomJWTBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

DATABASE_ROUTERS = ('apps.jwt_authentication.routers.MultiDatabaseRouter',)

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % PROJECT_NAME

# the URL for static files
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

DEBUG = STAGING = False

APPEND_SLASH = False

# CUSTOM DEPENDENCY
# pattern : ModuleName_ModelName_MODEL

# ### DATABASE CONFIGURATION ######################################
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
# ### EMAIL CONFIGURATION ###################################
EMAIL_USE_TLS = True
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = '%s Team <contact@%s>' % (PROJECT_NAME, PROJECT_DOMAIN)
EMAIL_HOST = getenv('EMAIL_HOST', '')
EMAIL_PORT = getenv('EMAIL_PORT', '')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', '')

# LOGGING CONFIG
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
# END LOGGING CONFIG


# Time tracking settings
# AUTH_PASSWORD_VALIDATORS = [
#     {H}
# ]
# End time tracking settings
