from django.core.management import call_command
from django.test import TestCase

from django_plus.management.commands.raise_test_exception import DjangoPlusTestException


class TestRaiseTestExceptionCommand(TestCase):
    def test_raise_test_exception(self):
        with self.assertRaises(DjangoPlusTestException):
            call_command('raise_test_exception')
