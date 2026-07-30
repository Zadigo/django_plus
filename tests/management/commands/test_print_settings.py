from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestPrintSettingsCommand(TestCase):
    def test_print_settings(self):
        out = StringIO()
        call_command('print_settings', stdout=out)
        output = out.getvalue()

        # Check that the output contains some known settings
        self.assertIn('DEBUG:', output)
        self.assertIn('INSTALLED_APPS:', output)

    def test_print_settings_with_filter(self):
        out = StringIO()
        call_command('print_settings', '--filter-by=DEBUG', stdout=out)
        output = out.getvalue()

        # Check that the output contains some known settings
        self.assertIn('DEBUG:', output)
        self.assertNotIn('INSTALLED_APPS:', output)
