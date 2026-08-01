import pathlib
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = "List all the files located in the MEDIA_ROOT"

    @signalcommand
    def handle(self, *args, **options):
        media_root: pathlib.Path = getattr(settings, 'MEDIA_ROOT', None)

        if isinstance(media_root, str):
            base_dir = getattr(settings, 'BASE_DIR', None)
            if base_dir is not None:
                media_root = base_dir / media_root

        if media_root is None:
            self.stdout.write(
                self.style.ERROR(
                    'MEDIA_ROOT is not set in settings.'
                )
            )
            return

        all_files: set[pathlib.Path] = set()
        structure = defaultdict(list)
        for item in media_root.rglob('*'):
            if item.is_dir():
                structure[item.parent].append(
                    '[DIR] ' +
                    self.style.NOTICE(
                        str(item.relative_to(media_root))
                    )
                )
                continue

            if item.is_file():
                all_files.add(item)
                files = structure[item.parent]
                files.append(
                    '[FILE] ' +
                    self.style.HTTP_INFO(
                        str(item.relative_to(media_root)))
                )

        self.stdout.write(self.style.SUCCESS(
            f'Files located in MEDIA_ROOT ({media_root}) - total {len(all_files)} files'
        ))

        for parent, items in structure.items():
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{parent.relative_to(media_root)} ({len(items)} files):'
                )
            )
            for item in items:
                self.stdout.write(f'+ {item}')

        # Get all the FileField for each model
        model_dict: defaultdict[models.Model,
                                list[models.FileField]] = defaultdict(list)
        for model in apps.get_models():
            for field in model._meta.fields:
                if issubclass(field.__class__, models.FileField):
                    model_dict[model].append(field)

        referenced_files = set()
        for model, field in model_dict.items():
            qs = model.objects.all()
            for item in qs:
                for f in field:
                    target_file = getattr(item, f.name)
                    if target_file:
                        referenced_files.add(target_file.path.absolute())
        unreferenced_files = all_files - referenced_files
        if unreferenced_files:
            self.stdout.write(
                self.style.WARNING(
                    '\nUnreferenced files in MEDIA_ROOT:'
                )
            )
            for f in unreferenced_files:
                self.stdout.write(
                    self.style.WARNING('- ') + str(f.relative_to(media_root))
                )
