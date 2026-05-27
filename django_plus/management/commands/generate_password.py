from typing import Sequence
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import password_validation
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Generate a random password using Django's built-in password generator."
    requires_system_checks: Sequence[str] = []

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--length',
            nargs='?',
            type=int,
            default=16,
            help='Password length.'
        )

    def handle(self, *args, **options):
        password_length = options.get('length', 16)

        # Generate a random password
        password = get_random_string(length=password_length)

        try:
            # Validate the password using Django's built-in validators
            password_validation.validate_password(password)
        except password_validation.ValidationError as e:
            raise CommandError(
                f'Generated password did not meet validation criteria: {e}'
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Generated password: {password}'
                )
            )
