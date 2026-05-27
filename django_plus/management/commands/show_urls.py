
from typing import Callable
import re
import functools
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ViewDoesNotExist
from django.urls import URLPattern, URLResolver
import enum
from collections import defaultdict


class FormatStyle(enum.Enum):
    DENSE = '{url}\t{module}\t{url_name}\t{decorator}'
    TABLE = None
    ALIGNED = None
    VERBOSE = None
    JSON = ""
    PRETTRY_JSON = ""


FORMAT_STYLES = list(FormatStyle.__members__.keys())


def extract_views_from_urlpatterns(urlpatterns: list, base: str = '', namespace: str = None):
    '''Returns a list of view functions from the given urlpatterns.'''
    views: list[tuple[Callable, str, str]] = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            try:
                if namespace is not None:
                    name = f'{namespace}:{pattern.name}'
                else:
                    name = pattern.name
                views.append((pattern.callback, base +
                             str(pattern.pattern.regex.pattern), name))
            except ViewDoesNotExist:
                continue

        if isinstance(pattern, URLResolver):
            try:
                patterns = pattern.url_patterns
            except ImportError:
                continue

            if namespace is not None:
                namespace = f'{namespace}:{pattern.namespace}'

            result = extract_views_from_urlpatterns(
                patterns,
                base + str(pattern.pattern.regex.pattern),
                namespace
            )
            views.extend(result)
    return views


class Command(BaseCommand):
    help = 'Displays all of the url matching routes for the project.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            '-f',
            dest='format_style',
            default='dense',
            help=f'Style of the output. Choices: {", ".join(FORMAT_STYLES)}',
        )
        parser.add_argument(
            '--group',
            '-g',
            action='store_true',
            help='Group URLs by their first path segment.',
        )
        parser.add_argument(
            '--filter',
            '-F',
            dest='filter_pattern',
            help='Filter URLs by a regex pattern.',
        )
        parser.add_argument(
            '--sort',
            '-s',
            action='store_true',
            help='Sort the output by URL.',
        )
        # parser.add_argument(
        #     '--sort',
        #     '-s',
        #     dest='sort',
        #     nargs='+',
        #     choices=['url', 'module', 'name'],
        #     default=['url'],
        #     help='Sort the output by the specified fields.',
        # )

    def handle(self, *args, **options):
        views = []
        if not hasattr(settings, 'ROOT_URLCONF'):
            raise CommandError('The setting ROOT_URLCONF is not defined.')

        try:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        except ImportError as e:
            raise CommandError(f'Error importing ROOT_URLCONF: {e}')

        format_style = options.get('format_style')
        filter_by = options.get('filter_pattern')

        groups = defaultdict(list)

        view_funcs = extract_views_from_urlpatterns(urlconf.urlpatterns)
        for view_func, url_pattern, name in view_funcs:
            global_funcs = {}

            if hasattr(view_func, '__globals__'):
                global_funcs = view_func.__globals__

            if hasattr(view_func, 'func_globals'):
                global_funcs = view_func.func_globals

            decorators = [
                item for item in global_funcs
                if item in global_funcs
            ]

            if isinstance(view_func, functools.partial):
                pass

            func_name = re.sub(
                r' at 0x[0-9a-f]+', '',
                repr(view_func)
            )

            if hasattr(view_func, 'view_class'):
                func_name = view_func.view_class

            if hasattr(view_func, '__name__'):
                func_name = view_func.__name__

            if hasattr(view_func, '__class__'):
                func_name = f"{view_func.__class__.__name__}()"

            module = f'{view_func.__module__}.{func_name}'
            url_name = name or ''

            url = simplify_regex(url_pattern)
            if filter_by is not None:
                if filter_by not in url or filter_by not in name:
                    continue

            decorator = ', '.join(decorators)

            # Url parts for grouping
            parts = url.strip('/').split('/')
            group_urls = groups[parts[0]]
            group_urls.append(
                FormatStyle[format_style.upper()].value.format(
                    url=self.style.WARNING(url),
                    module=module,
                    url_name=self.style.SUCCESS(url_name),
                    decorator=None,
                )
            )

            if format_style == 'json':
                views.append(
                    {
                        'url': url,
                        'module': module,
                        'name': url_name,
                        'decorators': decorator,
                    }
                )
            else:
                views.append(
                    FormatStyle[format_style.upper()].value.format(
                        url=self.style.WARNING(url),
                        module=module,
                        url_name=self.style.SUCCESS(url_name),
                        decorator=None,
                    )
                )

        sort_values = options['sort']

        if options['group']:
            for group, urls in groups.items():
                self.stdout.write(
                    self.style.HTTP_INFO(
                        f'Group: {group} ({len(urls)} URLs)'
                    )
                )

                sorted_values = urls.copy()
                if sort_values:
                    sorted_values.sort()

                for url in sorted_values:
                    self.stdout.write(f'\t + {url}')
                self.stdout.write('')
        else:
            self.stdout.write(
                self.style.HTTP_INFO(
                    f'Total URLs: {len(views)}'
                )
            )

            if sort_values:
                views.sort()
            return '\n'.join([view for view in views]) + '\n'
