import inspect
import pathlib
from collections import defaultdict
from collections.abc import Iterator

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.views import View

from django_plus.management.utils import signalcommand
from django_plus.utils.spacing import Spacing


class Command(BaseCommand):
    help = 'List all the views in the project'

    def _collect_view_file(self, files: Iterator[pathlib.Path]) -> Iterator[pathlib.Path]:
        for file in files:
            if file.is_dir():
                continue

            if file.suffix in ['.py'] and file.name == 'views.py':
                yield file

    def _print_views(self, views: dict[str, list[str]]):
        for app_name, klasses in views.items():
            self.stdout.write(self.style.SUCCESS(app_name))
            for klass in klasses:
                self.stdout.write(Spacing.TAB_MINUS.value + klass)

    @signalcommand
    def handle(self, *args, **options):
        registered_apps: list[str] = []
        for app in apps.get_app_configs():
            if app.name.startswith('django.contrib'):
                continue
            registered_apps.append(app.name)

        base_dir: pathlib.Path = getattr(settings, 'BASE_DIR', None)
        if base_dir is None:
            raise CommandError('BASE_DIR is not defined in settings.')

        listed_views = defaultdict(list)

        for app_name in registered_apps:
            try:
                mod = import_string(f'{app_name}.views')
            except Exception: # noqa
                continue

            klasses = inspect.getmembers(mod, inspect.isclass)
            for _, klass in klasses:
                if issubclass(klass, View):
                    listed_views[app_name].append(klass.__name__)

        # view_files = defaultdict(list)
        # for app_name in registered_apps:
        #     fullpath = base_dir.joinpath(app_name.replace('.', '/'))
        #     if not fullpath.exists():
        #         continue

        #     candidate = list(self._collect_view_file(fullpath.rglob('*')))
        #     if candidate:
        #         view_files[app_name].extend(candidate)

        # listed_views = defaultdict(list)

        # for app_name, files in view_files.items():
        #     mod = import_string(f'{app_name}.views')
        #     klasses = inspect.getmembers(mod, inspect.isclass)
        #     for _, klass in klasses:
        #         if issubclass(klass, View):
        #             listed_views[app_name].append(klass.__name__)

        self._print_views(listed_views)
