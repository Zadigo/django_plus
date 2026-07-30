import json
import pprint

import yaml
from django.conf import global_settings, settings
from django.core.management.base import BaseCommand

from django_plus.management.utils import signalcommand


class Command(BaseCommand):
    help = 'Prints the current Django settings to the console.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filter-by',
            help='Filter settings by a specific keyword (e.g., "DATABASE").'
        )
        parser.add_argument(
            '--show-types',
            action='store_true',
            help='Show the types of the settings values. Works in conjunction with --output-format=values.'
        )
        parser.add_argument(
            '--output-format',
            choices=['json', 'yaml', 'pprint', 'text', 'values'],
            default='values',
            help='The format to output the settings in (default: values).'
        )
        parser.add_argument(
            '--exclude-defaults',
            action='store_true',
            help='Exclude default Django settings from the output.'
        )
        parser.add_argument(
            '--group',
            action='store_true',
            help='Group settings by Django and custom settings.'
        )

    @signalcommand
    def handle(self, *args, **options):
        # Get all setting keys from the global settings which will
        # allow grouping by Django and custom settings.
        default_setting_keys = sorted(dir(global_settings))

        count = 0
        _setting_keys = sorted(dir(settings))

        # Cache the setting keys in order to count
        # how many settings are displayed after filtering.
        setting_keys = _setting_keys.copy()

        filter_by = options.get('filter_by')
        if filter_by:
            setting_keys = [
                key for key in _setting_keys
                if filter_by in key.lower()
            ]

        settings_dict = {
            key: getattr(settings, key)
            for key in _setting_keys if key.isupper()
        }

        show_types = options.get('show_types', False)
        output_format = options.get('output_format', 'values')
        match output_format:
            case 'json':
                print(json.dumps(settings_dict, indent=4, default=str))
            case 'yaml':
                print(yaml.dump(settings_dict, default_flow_style=False))
            case 'pprint':
                pprint.pprint(settings_dict)
            case 'text':
                pass
            case 'values':
                if options.get('group', False):
                    template = {'django': [], 'custom': []}
                    for setting in setting_keys:
                        if setting.isupper():
                            value = getattr(settings, setting)
                            if setting in default_setting_keys:
                                template['django'].append((setting, value))
                            else:
                                template['custom'].append((setting, value))

                    for group, items in template.items():
                        self.stdout.write(
                            self.style.NOTICE(
                                f'{group.upper()} SETTINGS:'
                            )
                        )
                        for setting, value in items:
                            text = self._get_text_display(
                                setting, value, show_types)
                            self.stdout.write(f'\t{text}')
                else:
                    for setting in setting_keys:
                        if setting.isupper():
                            count += 1
                            value = getattr(settings, setting)

                            text = self._get_text_display(
                                setting, value, show_types)
                            self.stdout.write(text)

        self.stdout.write(self.style.WARNING(
            f'Total settings: {len(setting_keys)}, Displayed: {count}'))

    def _get_text_display(self, key, value, show_types=False):
        if show_types:
            return f'+ {self.style.SUCCESS(key)}: {type(value).__name__}'
        else:
            return f'+ {self.style.SUCCESS(key)}: {value}'
