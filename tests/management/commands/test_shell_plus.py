from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from django_plus.utils.shell.runners import Plain


def test_plain_runner():
    instance = Plain()
    
    assert callable(instance)

    assert hasattr(instance, 'flags')
    assert hasattr(instance, 'name')
    assert hasattr(instance, 'help')

    runner = instance()

    assert callable(runner)


class TestShellPlusCommand(TestCase):
    def setUp(self):
        self.out = StringIO() 

    def test_create_shell(self):
        call_command('shell_plus', stdout=self.out, stderr=self.out)

