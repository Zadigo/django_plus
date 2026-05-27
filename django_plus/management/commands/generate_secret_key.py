from typing import Sequence

from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = 'Generates a new SECRET_KEY that can be used in a project settings file.'

    requires_system_checks: Sequence[str] = []

    @signalcommand
    def handle(self, *args, **options):
        return f'{self.style.SUCCESS("Generated SECRET_KEY:")} {get_random_secret_key()}'
