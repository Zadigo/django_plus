from io import StringIO
from unittest.mock import patch

from django.contrib.auth import password_validation
from django.core.management import call_command
from django.test import TestCase


class TestGeneratePasswordCommand(TestCase):
    def test_without_args(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('generate_password', stdout=mock_stdout)
            output = mock_stdout.getvalue()

        self.assertIsNotNone(output, output)

    def test_with_length_args(self):
        length = 20
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command(
                'generate_password',
                length=length,
                stdout=mock_stdout
            )
            output = mock_stdout.getvalue()

        self.assertIsNotNone(output, output)

    def test_with_invalid_password(self):
        with patch('django_plus.management.commands.generate_password.get_random_string', return_value='abc'):
            with self.assertRaises(password_validation.ValidationError):
                call_command('generate_password')


# def test_without_args(capsys):
#     call_command('generate_password')

#     out, err = capsys.readouterr()
#     assert out


# def test_with_length_args(capsys):
#     length = 20
#     call_command('generate_password', length=length)

#     out, err = capsys.readouterr()
#     assert len(out.rstrip("\n")) == length
