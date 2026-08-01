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

type ListedViews = dict[str, list[tuple[str, list[str]]]]

BASE_DJANGO_VIEWS = [
    'TemplateView',
    'RedirectView',
    'DetailView',
    'ListView',
    'CreateView',
    'DateDetailView',
    'DayArchiveView',
    'ArchiveIndexView',
    'DeleteView',
    'FormView',
    'UpdateView',
    'MonthArchiveView',
    'WeekArchiveView',
    'TodayArchiveView',
    'View',
    'YearArchiveView',
]


class Command(BaseCommand):
    help = 'List all the views in the project'

    def _collect_view_file(self, files: Iterator[pathlib.Path]) -> Iterator[pathlib.Path]:
        for file in files:
            if file.is_dir():
                continue

            if file.suffix in ['.py'] and file.name == 'views.py':
                yield file

    def _print_views(self, views: ListedViews):
        for app_name, klasses in views.items():
            self.stdout.write(self.style.SUCCESS(app_name))

            for klass, superclass_names in klasses:
                superclass_names_output = ' (' + ', '.join(superclass_names) + ')' if superclass_names else ''
                self.stdout.write(Spacing.TAB_MINUS.value + klass + self.style.MIGRATE_LABEL(superclass_names_output))

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

        counter: int = 0

        for app_name in registered_apps:
            try:
                mod = import_string(f'{app_name}.views')
            except Exception: # noqa
                continue

            listed_views: ListedViews = defaultdict(list)

            klasses = inspect.getmembers(mod, predicate=inspect.isclass)
            for _, klass in klasses:
                if issubclass(klass, View):
                    # Get the superclass of the view in order to get the
                    # the cateogry of the view (e.g., TemplateView, ListView, etc.)
                    superclass = filter(
                        lambda base: base.__name__ in BASE_DJANGO_VIEWS,
                        inspect.getmro(klass)
                    )

                    superclass_names = [base.__name__ for base in superclass]
                    listed_views[app_name].append((klass.__name__, superclass_names))
                    counter += 1

        self._print_views(listed_views)
        self.stdout.write('\n' + self.style.SUCCESS(f'Total views found: {counter}'))
