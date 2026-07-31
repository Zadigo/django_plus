import os
import pathlib

from django.core.management import call_command
from django.test import TestCase


class TestCleanPyc(TestCase):
    def setUp(self):
        self.testapp_root = pathlib.Path(__file__).parent.parent.parent / 'testapp'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_plus.settings'

    def test_dry_run(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clean_pyc', dry_run=True)

    def test_dry_run_with_optimize(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('clean_pyc', dry_run=True, optimize=True)
