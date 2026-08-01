
import pathlib
import re
from collections.abc import Iterator

from django.conf import settings
from django.core.management.base import BaseCommand

from django_plus.management.utils import signalcommand
from django_plus.utils.spacing import Spacing

START_REGEX = re.compile(
    r"\{?#[\s]*?(TODO|FIXME|BUG|HACK|WARNING|NOTE|XXX)[\s:]?(.+)"
)

END_REGEX = re.compile(
    r"(.*)#\}(.*)"
)


class Command(BaseCommand):
    help = 'Show all annotations like TODO, FIXME, BUG, HACK, WARNING, NOTE etc. in your py and HTML files.'
    label = 'annotation tag (TODO, FIXME, BUG, HACK, WARNING, NOTE...)'

    @signalcommand
    def handle(self, *args, **options):
        apps: list[str] = []
        for app in getattr(settings, 'INSTALLED_APPS', []):
            if app.startswith('django.contrib'):
                continue
            apps.append(app)

        # template_dirs = getattr(settings, 'TEMPLATES', [])[0].get('DIRS', [])
        base_dir: pathlib.Path = getattr(settings, 'BASE_DIR', None)

        for app in apps:
            fullpath = base_dir.joinpath(app)
            lines = self._iterate_files(app, fullpath.rglob('*.py'))
            if lines:
                for line in lines:
                    self.stdout.write(
                        self.style.SUCCESS(Spacing.TAB_PLUS.value) + line
                    )

    def _iterate_files(self, app: str, files: Iterator[pathlib.Path]):
        lines: list[str] = []

        _files = list(files)
        if len(_files) > 0:
            self.stdout.write(self.style.SUCCESS(f'{len(_files)} notes from "{app}" application:'))

        for file in _files:
            with file.open() as f:
                for linenumber, line in enumerate(f.readlines(), start=1):
                    if START_REGEX.search(line):
                        tag, message = START_REGEX.findall(line)[0]

                        text = ''
                        if END_REGEX.search(message.strip()):
                            text = END_REGEX.findall(message.strip())[0][0]
                        lines.append(
                            f'{self.style.MIGRATE_LABEL(tag)}: {file}:{linenumber} {text.strip()}'
                        )
        return lines
