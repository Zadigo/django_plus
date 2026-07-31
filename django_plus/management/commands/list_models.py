import inspect

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection

from django_plus.management.utils import signalcommand
from django_plus.utils.spacing import Spacing

DEFAULT_MODEL_METHODS = {
    "check",
    "clean",
    "clean_fields",
    "date_error_message",
    "delete",
    "from_db",
    "full_clean",
    "get_absolute_url",
    "get_deferred_fields",
    "prepare_database_save",
    "refresh_from_db",
    "save",
    "save_base",
    "serializable_value",
    "unique_error_message",
    "validate_unique",
}

class Command(BaseCommand):
    help = 'List all models in the project, optionally filtered by app label.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            '-m',
            action='store',
            dest='model',
            default=None,
            help='Specify a model to list information for (format: app_label.ModelName).',
        )
        parser.add_argument(
            '--database-type',
            '-d',
            action='store_true',
            dest='database_type',
            default=False,
            help='Include the database type of each field in the output.',
        )
        parser.add_argument(
            '--all-methods',
            '-a',
            action='store_true',
            dest='all_methods',
            default=None,
            help='Include all methods of the model in the output.',
        )

    @signalcommand
    def handle(self, *args, **options):
        model_name: str | None = options.get('model', None)

        models = apps.get_models()

        _sorted_models = sorted(models, key=lambda m: (m._meta.app_label, m._meta.model_name))

        for model in _sorted_models:
            fullname = f"{model._meta.app_label}.{model._meta.model_name}"

            if model_name is not None and fullname.lower() != model_name.lower():
                continue

            # Write the model's app label and model name to the output
            self.stdout.write(fullname)
            self.stdout.write(Spacing.TAB.value + self.style.NOTICE("Fields:"))

            # Write each field's name and class to the output, 
            # optionally including the database type
            for field in model._meta.get_fields():
                info = f"{field.name} - {field.__class__.__name__}"

                if options.get('database_type', False):
                    try:
                        info += f" (DB Type: {field.db_type(connection=connection)})"
                    except TypeError:
                        info += self.style.WARNING(" (DB Type: unknown)")
                    except AttributeError:
                        info += self.style.WARNING(" (DB Type: unknown)")

                self.stdout.write(Spacing.TAB.value * 2 + info)

            methods_message = "Methods {display}:"
            return_all_methods = options.get('all_methods', None)
            if return_all_methods is True:
                methods_message = methods_message.format(display="(all)")
            else:
                methods_message = methods_message.format(display="(default)")

            for name in dir(model):
                func = getattr(model, name, None)
                if func is None:
                    continue

                if not callable(func):
                    continue
                
                if return_all_methods:
                    # Get the signature of the method if possible aka
                    # the *args and **kwargs it accepts, otherwise 
                    # default to "()"
                    if not name[0].isupper():
                        signature = "()"

                        try:
                            signature = str(inspect.signature(func))
                        except (TypeError, ValueError):
                            signature = "()"
                        self.stdout.write(Spacing.TAB.value * 2 + f"{name}{signature} - built-in")
                else:
                    logic = all(
                        [
                            callable(func),
                            not name.startswith("_"),
                            name not in DEFAULT_MODEL_METHODS,
                            not name[0].isupper()
                        ]
                    )

                    if logic:
                        self.stdout.write(Spacing.TAB.value * 2 + f"{name}() - custom method")

            self.stdout.write(self.style.SUCCESS(f"Total models listed: {len(models)}"))
