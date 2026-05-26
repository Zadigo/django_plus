from django.core.management.base import BaseCommand, CommandError
from django_plus.management.utils import signalcommand
from django.conf import settings
import pathlib
from typing import Iterator, Sequence


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
            help='Remove optimized python bytecode files',
        )
        parser.add_argument(
            '--dry-run',
            '-d',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Show which files would be removed without actually deleting them',
        )
        parser.add_argument(
            '--path',
            '-p',
            action='store',
            dest='path',
            help='Specify path to recurse into',
        )

    @signalcommand
    def handle(self, *args, **options):
        custom_dir = options.get('path', None)
        if custom_dir is None:
            custom_dir: pathlib.Path = getattr(settings, 'BASE_DIR', None)

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

        for iterator in iterators:
            for item in iterator:
                if options.get('dry_run', False):
                    self.stdout.write(f'Would remove: {item}')
                    continue
                # else:
                #     try:
                #         item.unlink()
                #         self.stdout.write(f'Removed: {item}')
                #     except Exception as e:
                #         self.stderr.write(f'Error removing {item}: {e}')
