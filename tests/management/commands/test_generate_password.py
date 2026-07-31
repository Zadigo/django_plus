from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class TestGeneratePasswordCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_without_args(self):
        call_command('generate_password', stdout=self.out)
        output = self.out.getvalue()

        self.assertIsNotNone(output)

    def test_with_length_args(self):
        length = 20
        call_command(
            'generate_password',
            length=length,
            stdout=self.out
        )
        output = self.out.getvalue()

        self.assertIsNotNone(output, output)

    def test_with_invalid_password(self):
        with self.assertRaises(CommandError):
            call_command('generate_password', length=1, stdout=self.out)
