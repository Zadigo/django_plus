from collections.abc import Sequence
from enum import Enum

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand

from django_plus.management.utils import signalcommand
from django_plus.typings import UserModelValuesQueryset


class ExportFormat(Enum):
    ADDRESS = 'address'
    EMAILS = 'emails'
    GOOGLE = 'google'
    OUTLOOK = 'outlook'
    # LINKEDIN = 'linkedin'
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
        items = [item.get('email', '') for item in queryset]
        self.stdout.write('\n'.join(items))

    def _export_google(self, queryset: UserModelValuesQueryset):
        columns = [
            'Email',
            'Phone',
            'First Name',
            'Last Name',
            'Country',
            'Zip'
        ]

        for item in queryset:
            result = {k: '' for k in columns}

            result['Email'] = item.get('email', '')
            result['Phone'] = item.get('mobile_phone', '')
            result['First Name'] = item.get('first_name', '')
            result['Last Name'] = item.get('last_name', '')
            result['Country'] = item.get('country', '')
            result['Zip'] = item.get('postal_code', '')

            self.stdout.write(','.join(result.values()))

    def _export_outlook(self, queryset: UserModelValuesQueryset):
        columns = [
            'First Name',
            'Last Name',
            'Full Name',
            'Title',
            'E-mail Address',
            'Email 2 Address',
            'Business Phone',
            'Home Phone',
            'Company',
            'Job Title',
            'Mobile Phone',
            'Fax Number',
            'Address',
            'City',
            'State/Province',
            'ZIP/Postal Code',
            'Country/Region',
            'Web Page',
            'Notes',
        ]

        rows: list[list[str]] = []

        for item in queryset:
            result = {k: '' for k in columns}

            result['First Name'] = item.get('first_name', '')
            result['Last Name'] = item.get('last_name', '')
            result['Full Name'] = item.get('get_full_name', '')
            result['E-mail Address'] = item.get('email', '')

            rows.append(list(result.values()))

        self.stdout.write('\n'.join(','.join(row) for row in rows))

    # def _export_linkedin(self, queryset: UserModelValuesQueryset):
    #     # Implement the logic to export in LinkedIn format
    #     pass

    def _export_vcard(self, queryset: UserModelValuesQueryset):
        try:
            import vobject
        except ImportError:
            self.stderr.write("vobject library is required for vCard export. Please install it using 'pip install vobject'.")
            return
        else:
            for item in queryset:
                card = vobject.vCard()

                # card.add('fn').value = item.get('get_full_name', '')
                # card.add('n').value = vobject.vcard.Name(
                #     family=item.get('last_name', ''),
                #     given=item.get('first_name', '')
                # )
                # email_part = card.add('email')
                # email_part.value = item.get('email', '')

                # Add name components
                card.add('n')

                firstname = item.get('first_name', '')
                lastname = item.get('last_name', '')
                card.n.value = vobject.vcard.Name(family=lastname, given=firstname)
                card.add('fn')
                card.fn.value = f'{firstname} {lastname}'

                # Add contact details
                # card.add('tel')
                # card.tel.value = item.get('mobile_phone', None)
                # card.tel.type_param = 'CELL'

                card.add('email')
                card.email.value = item.get('email', '')
                card.email.type_param = 'WORK'

                # card.adr.value = vobject.vcard.Address(
                #     street="123 Science Way",
                #     city="Boston",
                #     region="MA",
                #     code="02108",
                #     country="USA"
                # )
                # card.adr.type_param = 'WORK'

                self.stdout.write(card.serialize())

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            '-f',
            action='store',
            dest='format',
            default=ExportFormat.ADDRESS.value,
            help='Specifies the export format. Supported formats: ' + ', '.join(EXPORT_FORMATS_MAP)
        )
        parser.add_argument(
            '--group',
            '-g',
            action='store',
            dest='group',
            help='Specifies the group to filter users by.'
        )
        parser.add_argument(
            '--active-users',
            '-a',
            action='store_true',
            dest='active_users',
            help='If set, only active users will be exported.'
        )
        # parser.add_argument(
        #     'output_file',
        #     nargs='?',
        #     type=str,
        #     default=None,
        #     help='Optional output file to save the exported data. If not provided, output will be printed to stdout.'
        # )

    @signalcommand
    def handle(self, *args, **options):
        group = options.get('group', None)

        default_order_by = ['last_name', 'first_name']
        order_by = getattr(
            settings,
            'DJANGO_PLUS_EXPORT_EMAILS_ORDER_BY',
            default_order_by
        )

        queryset = self.user_model.objects.order_by(*order_by)
        if options.get('active_users', False):
            queryset = queryset.filter(is_active=True)

        if group is not None:
            queryset = queryset.filter(groups__name=group)
            
        default_fields = ['first_name', 'last_name', 'email']
        fields = getattr(
            settings,
            'DJANGO_PLUS_EXPORT_EMAILS_FIELDS',
            default_fields
        )

        try:
            qs = queryset.values(*fields)
        except FieldError as e:
            raise ExceptionGroup(
                'Error while retrieving user data for export', [e]
            )

        # Call the appropriate export method based on the specified format
        getattr(self, f'_export_{options["format"]}')(qs)
