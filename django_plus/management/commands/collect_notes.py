
import pathlib
import re
from collections.abc import Iterator

from django.conf import settings
from django.core.management.base import BaseCommand

from django_plus.management.utils import signalcommand

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
            lines = self._iterate_files(fullpath.rglob('*.py'))
            if lines:
                for line in lines:
                    self.stdout.write(
                        self.style.SUCCESS("   + ") + line
                    )

    def _iterate_files(self, files: Iterator[pathlib.Path]):
        lines: list[str] = []

        _files = list(files)
        if len(_files) > 0:
            self.stdout.write(f'Collecting notes from {len(_files)} files...')

        for file in _files:
            with file.open() as f:
                linenumber = 0
                for line in f.readlines():
                    linenumber += 1
                    if START_REGEX.search(line):
                        tag, message = START_REGEX.findall(line)[0]

                        text = ''
                        if END_REGEX.search(message.strip()):
                            text = END_REGEX.findall(text.strip())[0][0]
                        lines.append(
                            f'{file}:{linenumber} {tag} {text.strip()}')
        return lines
