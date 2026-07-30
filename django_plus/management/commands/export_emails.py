from collections.abc import Sequence
from enum import Enum

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django_plus.typings import UserModelValuesQueryset


class ExportFormat(Enum):
    ADDRESS = 'address'
    EMAILS = 'emails'
    GOOGLE = 'google'
    OUTLOOK = 'outlook'
    LINKEDIN = 'linkedin'
    VCARD = 'vcard'


EXPORT_FORMATS_MAP = [format.value for format in ExportFormat]


class Command(BaseCommand):
    help = 'Command used to export emails from the system.'
    requires_system_checks: Sequence = []

    _template = '"{full_name}" <{email}>;'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def _export_address(self, queryset: UserModelValuesQueryset):
        """Returns a string with the email addresses in the format:
        .. text::
            "full name" <my@address.com>;
        """
        items = []
        for item in queryset:
            full_name = item.get('get_full_name')
            if full_name is None:
                firstname = item.get('first_name', '')
                lastname = item.get('last_name', '')
                full_name = f"{firstname} {lastname}".strip()

            value = self._template.format(
                full_name=full_name,
                email=item.get('email', '')
            )

            items.append(value)
        self.stdout.write('\n'.join(items))

    def _export_emails(self, queryset: UserModelValuesQueryset):
        # Implement the logic to export in emails format
        pass

    def _export_google(self, queryset: UserModelValuesQueryset):
        # Implement the logic to export in Google format
        pass

    def _export_outlook(self, queryset: UserModelValuesQueryset):
        # Implement the logic to export in Outlook format
        pass

    def _export_linkedin(self, queryset: UserModelValuesQueryset):
        # Implement the logic to export in LinkedIn format
        pass

    def _export_vcard(self, queryset: UserModelValuesQueryset):
        # Implement the logic to export in vCard format
        pass

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            '-f',
            action='store',
            dest='format',
            default=ExportFormat.ADDRESS.value,
            help='Specifies the export format. Supported formats: ' +
            ', '.join(EXPORT_FORMATS_MAP)
        )

    def handle(self, *args, **options):
        group = None

        default_order_by = ['last_name', 'first_name']
        order_by = getattr(
            settings,
            'DJANGO_PLUS_EXPORT_EMAILS_ORDER_BY',
            default_order_by
        )

        queryset = self.user_model.objects.order_by(*order_by)
        if group is not None:
            pass

        default_fields = ['first_name', 'last_name', 'email']
        fields = getattr(
            settings,
            'DJANGO_PLUS_EXPORT_EMAILS_FIELDS',
            default_fields
        )
        queryset = queryset.values(*fields)
        # Call the appropriate export method based on the specified format
        getattr(self, f'_export_{options["format"]}')(queryset)
