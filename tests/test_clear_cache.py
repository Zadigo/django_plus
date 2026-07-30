import os
import pathlib

from django.core.management import call_command
from django.test import TestCase


class TestClearCache(TestCase):
    def setUp(self):
        self.testapp_root = pathlib.Path(__file__).parent / 'testapp'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_plus.settings'

    def test_dry_run(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clear_cache')
