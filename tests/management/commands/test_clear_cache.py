import pathlib
from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase


class TestClearCache(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.testapp_root = pathlib.Path(__file__).parent.parent.parent / 'testapp'

    def test_dry_run(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clear_cache', stdout=self.out)

    def test_clear_all_caches(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clear_cache', all=True, stdout=self.out)

    def test_with_invalid_cache(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clear_cache', cache='invalid_cache', stdout=self.out, stderr=self.out)

            result = self.out.getvalue()
            self.assertIn('Error clearing cache', result)

    def test_with_both_cache_and_all(self):
        with self.settings(BASE_DIR=self.testapp_root):
            with self.assertRaises(CommandError):
                call_command('clear_cache', cache='default', all=True, stdout=self.out, stderr=self.out)

                result = self.out.getvalue()
                self.assertIn('Cannot specify both --cache and --all options.', result)
