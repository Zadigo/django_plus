from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from django.test.utils import override_settings
import pathlib

TEST_DIR = pathlib.Path(__file__).parent.parent.parent


@override_settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django_plus', 'tests.testapp'])
class TestListViewsCommand(TestCase):
    def test_list_views_command(self):
        out = StringIO()
        call_command('list_views', stdout=out)
        output = out.getvalue()

        self.assertIn('App: tests.testapp', output)
        self.assertIn('  - HomeView', output)
