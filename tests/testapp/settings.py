import pathlib

import environ
from faker import Faker

environ.Env.read_env('../.env')

env = environ.Env()

fake = Faker()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = f'dummy-insecure-{fake.uuid4()}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests.testapp',
    'django_plus',
    # 'tests.collisions',
    # 'tests.testapp_with_no_models_file',
    # 'tests.testapp_with_appconfig.apps.TestappWithAppConfigConfig',
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

ROOT_URLCONF = 'tests.testapp.urls'

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': TEMPLATE_DEBUG,
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tests.testapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

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

# DATABASES={
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = BASE_DIR / 'django_plus/tmp/'

MEDIA_PATH = BASE_DIR / 'media/'

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
