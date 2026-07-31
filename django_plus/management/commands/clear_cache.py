from collections.abc import Sequence

from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.management.base import BaseCommand, CommandError

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = 'Command that clears the cache for all the cache backends configured in the project.'
    requires_system_checks: Sequence = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--cache',
            action='append',
            help='Name of cache to clear'
        )
        parser.add_argument(
            '--all',
            '-a',
            action='store_true',
            default=False,
            dest='all_caches',
            help='Clear all configured caches',
        )

    @signalcommand
    def handle(self, cache: str | None = None, all_caches: bool = False, *args, **kwargs):
        if cache is None and not all_caches:
            cache = [DEFAULT_CACHE_ALIAS]
        elif cache is not None and all_caches:
            raise CommandError(
                'Cannot specify both --cache and --all options.'
            )
        elif all_caches:
            cache = getattr(
                settings,
                'CACHES', {
                    DEFAULT_CACHE_ALIAS: {}}
            ).keys()

        for key in cache:
            try:
                caches[key].clear()
                self.stdout.write(f'Cleared cache: {key}')
            except InvalidCacheBackendError as e:
                self.stderr.write(f'Error clearing cache {key}: {e}')
            else:
                self.stdout.write(f'Successfully cleared cache: {key}')
