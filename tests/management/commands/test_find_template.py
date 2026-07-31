import pathlib
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestFindTemplate(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.testapp_dir = pathlib.Path(__file__).parent.parent.parent.parent / 'tests' / 'testapp'
        
    def test_find_template(self):
        with self.settings(BASE_DIR=self.testapp_dir, INSTALLED_APPS=['django_plus', 'tests.testapp']):
            call_command('find_template', 'home.html', stdout=self.out)

            output = self.out.getvalue()
            self.assertIn('home.html', output)

    def test_find_template_not_found(self):
        with self.settings(BASE_DIR=self.testapp_dir, INSTALLED_APPS=['django_plus', 'tests.testapp']):
            call_command('find_template', 'non_existent_template.html', stderr=self.out)

            output = self.out.getvalue()
            self.assertIn('No template found', output)
