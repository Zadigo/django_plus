from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestGenerateSecretKeyCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_without_args(self):
        call_command('generate_secret_key', stdout=self.out)
        output = self.out.getvalue()

        self.assertIsNotNone(output)

    def test_secret_key_generation(self):
        call_command('generate_secret_key', stdout=self.out)
        output = self.out.getvalue()

        self.assertIsNotNone(output)
