import pathlib
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings

TEST_DIR = pathlib.Path(__file__).parent.parent.parent.parent.absolute()


@override_settings(BASE_DIR=TEST_DIR)
class TestCollectNotesCommand(TestCase):
    def test_collect_notes_command(self):
        with self.settings(INSTALLED_APPS=['django_plus']):
            out = StringIO()
            call_command('collect_notes', stdout=out)
            output = out.getvalue()
            self.assertIn('Collecting notes from', output)
