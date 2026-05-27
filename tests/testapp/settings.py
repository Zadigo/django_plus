import environ
import pathlib

environ.Env.read_env('../.env')

env = environ.Env()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'dummy'

# TEST_RUNNER = 'tests.runner.PytestTestRunner'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sites',
    # 'tests.collisions',
    'tests.testapp',
    # 'tests.testapp_with_no_models_file',
    # 'tests.testapp_with_appconfig.apps.TestappWithAppConfigConfig',
    'django_plus',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': env('DJANGO_PLUS_DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DJANGO_PLUS_DATABASE_NAME', default=':memory:'),
        'USER': env('DJANGO_PLUS_DATABASE_USER', default=''),
        'PASSWORD': env('DJANGO_PLUS_DATABASE_PASSWORD', default=''),
        'HOST': env('DJANGO_PLUS_DATABASE_HOST', default=''),
        'PORT': env('DJANGO_PLUS_DATABASE_PORT', default=''),
    }
}

SITE_ID = 1

MEDIA_ROOT = BASE_DIR / 'django_plus/tmp/'

MEDIA_PATH = '/media/'

ROOT_URLCONF = 'tests.testapp.urls'

DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': TEMPLATE_DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'

# SHELL_PLUS_SUBCLASSES_IMPORT_MODULES_BLACKLIST = [
#     'django_extensions.mongodb.fields',
#     'django_extensions.mongodb.models',
#     'tests.testapp.scripts.invalid_import_script',
#     'setup',
# ]

# CACHES = {
#     'default': {
#         'BACKEND': 'tests.management.commands.test_clear_cache.DefaultCacheMock',
#     },
#     'other': {
#         'BACKEND': 'tests.management.commands.test_clear_cache.OtherCacheMock',
#     },
# }

# SHELL_PLUS_PRE_IMPORTS = [
#     'import sys, os',
# ]
# SHELL_PLUS_IMPORTS = [
#     'from django_extensions import settings as django_extensions_settings',
# ]
# SHELL_PLUS_POST_IMPORTS = [
#     'import traceback',
#     'import pprint',
#     'import os as test_os',
#     'from django_extensions.utils import *',
#     'import http.client',
# ]

# SILENCED_SYSTEM_CHECKS = ['models.W027', 'models.W042']
