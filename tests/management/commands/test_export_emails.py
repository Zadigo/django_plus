import pathlib
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

TEST_DIR = pathlib.Path(__file__).parent.parent.parent.parent.absolute()


# @override_settings(BASE_DIR=TEST_DIR)
class TestExportEmailsCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword'
        )
        
    def test_export_emails_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='address', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('"', output)
