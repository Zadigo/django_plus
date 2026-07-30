import pathlib
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

TEST_DIR = pathlib.Path(__file__).parent.parent.parent

class TestLoadUsersCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_load_from_file(self):
        with self.settings(BASE_DIR=TEST_DIR):
            call_command('load_users', filename='users', stdout=self.out)
            self.assertIn('Successfully loaded', self.out.getvalue())

    def test_load_from_url(self):
        pass

    def test_with_format_values(self):
         with self.settings(BASE_DIR=TEST_DIR):
            call_command('load_users', format_values=True, filename='users', stdout=self.out)
            self.assertIn('Successfully loaded', self.out.getvalue())

    def test_with_make_active(self):
        with self.settings(BASE_DIR=TEST_DIR):
            call_command('load_users', make_active=True, filename='users', stdout=self.out)
            self.assertIn('Successfully loaded', self.out.getvalue())

    def test_dry_run(self):
        pass

    def test_set_password(self):
        with self.settings(BASE_DIR=TEST_DIR):
            call_command('load_users', set_password=True, filename='users', stdout=self.out)
            self.assertIn('Successfully loaded', self.out.getvalue())
