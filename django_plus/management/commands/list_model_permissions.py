from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models.functions import Lower

from django_plus.utils.spacing import Spacing


class Command(BaseCommand):
    help = "List all permissions for models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--by-app-label",
            nargs="*",
            help="[app_label.]model(s) to show permissions for.",
        )
        

    def handle(self, *args, **options):
        by_app_label = options.get("by_app_label")

        qs = ContentType.objects.order_by("app_label", Lower("model"))

        if by_app_label is not None:
            qs = qs.filter(app_label__in=by_app_label)
            if not qs.exists():
                self.stdout.write(
                    self.style.ERROR(
                        f"No content types found for app label(s) '{', '.join(by_app_label)}'."
                    )
                )
                return

        for content_type in qs:
            self.stdout.write(self.style.SUCCESS(f"Permissions for {content_type}"))

            for perm in content_type.permission_set.all():
                self.stdout.write(Spacing.TAB.value + f"{content_type.app_label}.{perm.codename} | {perm.name}")
