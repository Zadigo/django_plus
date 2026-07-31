import pathlib
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestListModelsCommand(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.testapp_root = pathlib.Path(__file__).parent.parent.parent / 'testapp'

    def test_list_models_no_options(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('list_models', stdout=self.out)

            result = self.out.getvalue()
            self.assertIn('admin.logentry', result)

    def test_list_models_with_model_option(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('list_models', model='admin.logentry', stdout=self.out)

            result = self.out.getvalue()
            self.assertIn('admin.logentry', result)

    def test_list_models_with_database_type_option(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('list_models', database_type=True, stdout=self.out)

            result = self.out.getvalue()
            self.assertIn('admin.logentry', result)

    def test_list_models_with_all_methods_option(self):
        with self.settings(BASE_DIR=self.testapp_root):
            call_command('list_models', all_methods=True, stdout=self.out)

            result = self.out.getvalue()
            self.assertIn('admin.logentry', result)
