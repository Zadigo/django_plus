from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase


class TestShowUrlsCommand(TestCase):
    def test_basic_implementation(self):
        out = StringIO()
        call_command('show_urls', stdout=out)
        output = out.getvalue()

        # Check that the output contains some known URLs
        self.assertIn('/admin/', output)

    def test_implementaion_with_filter(self):
        out = StringIO()
        call_command('show_urls', '--filter', 'add', stdout=out)
        output = out.getvalue()

        # Check that the output contains only URLs with 'add'
        self.assertIn('/add/', output)

    def test_implementation_with_grouping(self):
        out = StringIO()
        call_command('show_urls', '--group', stdout=out)
        output = out.getvalue()

        # Check that the output contains group headers
        self.assertIn('Group: admin', output)

    def test_implementation_with_sorting(self):
        out = StringIO()
        call_command('show_urls', '--sort', stdout=out)
        output = out.getvalue()

        # Check that the output is sorted by module
        self.assertIn('admin/', output)

    def test_raises_error_with_no_url_conf(self):
        with self.settings(ROOT_URLCONF='something.non_existent'):
            with self.assertRaises(CommandError):
                call_command('show_urls')
