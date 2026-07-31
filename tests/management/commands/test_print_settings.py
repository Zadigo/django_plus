from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestPrintSettingsCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_print_settings(self):
        call_command('print_settings', stdout=self.out)
        output = self.out.getvalue()

        # Check that the output contains some known settings
        self.assertIn('DEBUG:', output)
        self.assertIn('INSTALLED_APPS:', output)

    def test_print_settings_with_filter(self):
        call_command('print_settings', filter_by='DEBUG', stdout=self.out)

        output = self.out.getvalue()

        # Check that the output contains some known settings
        self.assertIn('DEBUG:', output)
        self.assertNotIn('INSTALLED_APPS:', output)

    def test_print_formats(self):
        formats = ['json', 'yaml', 'pprint', 'text', 'values', 'values_group']
        for fmt in formats:
            with self.subTest(fmt=fmt):
                if fmt == 'values_group':
                    call_command('print_settings', output_format='values', group=True, stdout=self.out)
                else:
                    call_command('print_settings', output_format=fmt, stdout=self.out)

                output = self.out.getvalue()
                self.assertTrue(output)  # Ensure some output is produced
                self.out.truncate(0)
                self.out.seek(0)
