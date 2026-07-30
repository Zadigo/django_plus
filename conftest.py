from django.conf import settings


def pytest_configure(config):

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='aXDfw6xCDKIFRgz2yzpTgAqFBqVLgSeyOVGayj8KqcJAjG3O96dT7cQPMExxAteX',
            PY_UTILITIES_JWT_SECRET='zpDaqupaQR7SxrEcsoFYOkZQIdJPEim4Sz30zC5oBFGOZwY92FYvVeqqO3Z5Pw6P',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django_plus',
                'tests.testapp',
            ],
            # AUTH_USER_MODEL='auth.User',
            ROOT_URLCONF='tests.testapp.urls',
            DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
            MEDIA_ROOT='/django_plus/tmp/',
            STATIC_URL='/static/'
        )
