
from django.core.management.base import LabelCommand
from django.template import TemplateDoesNotExist, loader

from django_plus.management.utils import signalcommand


class Command(LabelCommand):
    help = 'Finds the location of the given template by resolving its path'
    args = '[template_path]'
    label = 'template path'

    @signalcommand
    def handle_label(self, template_path, **options):
        try:
            template = loader.get_template(template_path).template
        except TemplateDoesNotExist:
            self.stderr.write(self.style.WARNING('No template found\n'))
        else:
            message = f'Template {template.name} found at: {self.style.NOTICE(template.origin.name)}\n'
            self.stdout.write(message)
