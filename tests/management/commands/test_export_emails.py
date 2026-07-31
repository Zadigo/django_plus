import pathlib
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase, override_settings

TEST_DIR = pathlib.Path(__file__).parent.parent.parent.parent.absolute()


@override_settings(BASE_DIR=TEST_DIR)
class TestExportEmailsCommand(TestCase):
    def setUp(self):
        self.out = StringIO()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword',
            is_active=True
        )

        new_group = Group.objects.create(name='testgroup')
        new_group.user_set.add(user)

    def test_export_with_group(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='address', group='testgroup', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)
        
    def test_export_emails_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='address', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)

    def test_export_outlook_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='outlook', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)

    def test_export_vcard_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='vcard', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)

    def test_export_google_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='google', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)

    def test_export_address_command(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp']):
            call_command('export_emails', format='address', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)

    def test_DJANGO_PLUS_EXPORT_EMAILS_FIELDS(self):
        with self.settings(BASE_DIR=TEST_DIR, INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django_plus', 'tests.testapp'], DJANGO_PLUS_EXPORT_EMAILS_FIELDS=['email']):
            call_command('export_emails', format='address', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('testuser1@example.com', output)
