from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestShellPlusCommand(TestCase):
    def setUp(self):
        self.out = StringIO() 

    def test_create_shell(self):
        call_command('shell_plus', stdout=self.out, stderr=self.out)

