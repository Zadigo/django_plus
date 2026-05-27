# Based on https://gist.github.com/voldmar/1264102
# and https://gist.github.com/runekaagaard/2eecf0a8367959dc634b7866694daf2c

import gc
import inspect
import weakref
from collections import defaultdict
from django.utils.encoding import force_str
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models.signals import (
    ModelSignal,
    pre_init,
    post_init,
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
    pre_migrate,
    post_migrate,
)


SIGNAL_NAMES = {
    pre_init: 'pre_init',
    post_init: 'post_init',
    pre_save: 'pre_save',
    post_save: 'post_save',
    pre_delete: 'pre_delete',
    post_delete: 'post_delete',
    m2m_changed: 'm2m_changed',
    pre_migrate: 'pre_migrate',
    post_migrate: 'post_migrate',
}


class Command(BaseCommand):
    help = 'List all signals by model and signal type'

    def handle(self, *args, **options):
        model_types = apps.get_models(
            include_auto_created=True, 
            include_swapped=True
        )
        models_map = {id(model): model for model in model_types}

        signals = [
            item for item in gc.get_objects() 
            if isinstance(item, ModelSignal)
        ]
        
        models = defaultdict(lambda: defaultdict(list))

        for signal in signals:
            name = SIGNAL_NAMES.get(signal, 'unknown')
            for receiver in signal.receivers:
                lookup, receiver, _sender, is_async = receiver

                if isinstance(receiver, weakref.ReferenceType):
                    receiver = receiver()

                if receiver is None:
                    continue

                receiver_id, sender_id = lookup
                model = models_map.get(sender_id, '_unknown_')
                if model:
                    template = '{module}.{name} #{line}{is_async}'
                    models[model][name].append(
                        template.format(
                            name=receiver.__name__,
                            module=receiver.__module__,
                            is_async=" (async)" if is_async else "",
                            line=inspect.getsourcelines(receiver)[1],
                            path=inspect.getsourcefile(receiver)
                        )
                    )

        output = []
        for key in sorted(models.keys(), key=str):
            verbose_name = force_str(key._meta.verbose_name)
            output.append(
                self.style.SUCCESS(
                    f"{key.__module__}, {key.__name__} ({verbose_name})"
                )
            )

            for signal_name, receivers in models[key].items():
                lines = models[key][signal_name]
                output.append(f"  {self.style.HTTP_INFO(signal_name)}:")

                for line in lines:
                    output.append(f"        {line}")

        return "\n".join(output)
