import pathlib
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestListSignals(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.testapp_root = pathlib.Path(__file__).parent.parent.parent / 'testapp'

    def test_list_signals(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('list_signals', stdout=self.out)

            result = self.out.getvalue()
            self.assertIn('tests.testapp.models.post_save_receiver', result)

