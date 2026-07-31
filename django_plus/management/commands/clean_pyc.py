import pathlib
from collections.abc import Iterator, Sequence

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = 'Removes all python bytecode compiled files from the project.'
    requires_system_checks: Sequence = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--optimize',
            '-o',
            '-O',
            action='store_true',
            dest='optimize',
            default=False,
            help='Remove .pyo files in addition to .pyc files',
        )
        parser.add_argument(
            '--dry-run',
            '-d',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Show what files would be removed without actually deleting them',
        )
        parser.add_argument(
            '--path',
            '-p',
            action='store',
            dest='path',
            help='Specify a custom path to search for .pyc and .pyo files. Defaults to BASE_DIR in settings.',
        )

    @signalcommand
    def handle(self, *args, **options):
        custom_dir = options.get('path', None)
        if custom_dir is None:
            custom_dir: pathlib.Path = getattr(settings, 'BASE_DIR', None)

        if isinstance(custom_dir, str):
            custom_dir = settings.BASE_DIR.joinpath(custom_dir)

        if custom_dir is None:
            raise CommandError(
                'No path provided and BASE_DIR not set in settings.'
            )

        iterators: list[Iterator[pathlib.Path]] = []
        items = custom_dir.rglob('*.pyc')
        iterators.append(items)

        if options.get('optimize', False):
            items = custom_dir.rglob('*.pyo')
            iterators.append(items)

        count = 0
        for iterator in iterators:
            for item in iterator:
                if options.get('dry_run', False):
                    self.stdout.write(f'- {self.style.WARNING(item)}')
                    count += 1
                    continue
                else:
                    try:
                        item.unlink()
                        self.stdout.write(f'Removed: {item}')
                    except FileNotFoundError as e:
                        self.stderr.write(f'Error removing {item}: {e}')
        self.stdout.write(
            self.style.SUCCESS(
                f'Found {count} files to remove.'
            )
        )
