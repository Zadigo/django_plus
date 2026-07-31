from django.core.management.base import BaseCommand

from django_plus.management.utils import signalcommand


class DjangoPlusTestException(Exception):
    pass


class Command(BaseCommand):
    help = "Raises a test Exception named DjangoPlusTestException for testing error reporting integrations."

    @signalcommand
    def handle(self, *args, **options):
        message = "Test exception raised via the django-plus raise_test_exception management command."
        raise DjangoPlusTestException(message)
