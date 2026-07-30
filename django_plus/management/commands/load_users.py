import csv
import pathlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import models

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = 'Load a set of users into the system using a csv or an url file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            help='Name of the file containing the users to load. Can be a local path or a URL.'
        )
        parser.add_argument(
            '--url',
            type=str,
            help='URL to the file containing the users to load.'
        )
        parser.add_argument(
            '--format-values',
            action='store_true',
            help='If set, the values from the file will be normalized before being saved in the database.'
        )
        parser.add_argument(
            '--make-active',
            action='store_true',
            help='If set, the loaded users will be marked as active in the system.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='If set, the command will simulate the loading of users without actually saving them to the database.'
        )
        parser.add_argument(
            '--set-password',
            type=str,
            help='If set, the loaded users will have their password set to the provided value.'
        )

    @signalcommand
    def handle(self, *args, **options):
        endpoint: str = options.get('url', None)
        file_path: str = options.get('filename', None)

        if file_path is None and endpoint is None:
            raise CommandError(
                'You must provide either a file path or a URL to load the users from.'
            )

        if file_path is not None and endpoint is not None:
            raise CommandError(
                'You cannot provide both a file path and a URL to load the users from. Please choose one.'
            )

        base_dir: pathlib.Path = settings.BASE_DIR
        file_path: pathlib.Path = base_dir.joinpath(f'{file_path}.csv')

        base_fields = ['first_name', 'last_name', 'email', 'username']

        if not file_path.exists():
            raise CommandError(f'The file {file_path} does not exist.')
        else:
            with file_path.open() as f:
                self.stdout.write(
                    self.style.HTTP_INFO(
                        f'Loading users from file: {file_path}'
                    )
                )

                users: list[User] = []

                reader = csv.DictReader(f, fieldnames=base_fields)
                for row in reader:
                    if not options['dry_run']:
                        defaults = {
                            'first_name': row.get('first_name', ''),
                            'last_name': row.get('last_name', ''),
                            'email': row.get('email', ''),
                            'username': row.get('username', ''),
                            'is_active': False
                        }

                        if options['format_values']:
                            defaults = {k: v.strip().title()
                                        for k, v in defaults.items()}

                        user_model = get_user_model()

                        qs = user_model.objects.filter(email=row['email'])
                        if qs.exists():
                            self.stdout.write(
                                self.style.WARNING(
                                    f'User with email {row["email"]} already exists. Updating existing user.'
                                )
                            )

                            user_model.objects.filter(
                                email=row['email']).update(**defaults)
                            user = qs.get()
                        else:
                            user = user_model.objects.create_user(**defaults)

                        if options['make_active']:
                            user.is_active = ~models.F('is_active')
                            user.save()

                        if options['set_password']:
                            user.set_password(options['set_password'])
                            user.save()

                        users.append(user)
                    else:
                        users.append(get_user_model()(**row))

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully loaded {len(users)} users from file: {file_path}'
                    )
                )
