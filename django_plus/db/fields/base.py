import string
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import CharField
from django.utils.crypto import get_random_string

# The maximum number of attempts to generate
# a unique value before giving up.
MAX_UNIQUE_TRIES: int = getattr(
    settings, 'DJANGO_PLUS_MAX_UNIQUE_TRIES', 100
)


class UniqueFieldMixin:
    @staticmethod
    def _get_fields(model_cls: models.Model):
        """Yields all fields of the model that are relations, one-to-one, 
        or many-to-one with a related model."""
        for field in model_cls._meta.get_fields():
            if field.is_relation or field.one_to_one or (field.many_to_one and field.related_model):
                yield field, field.model if field.model != model_cls else None

    def get_queryset(self, model_cls: models.Model, slug_field: models.Field):
        """Returns a queryset of all instances of the model that have a 
        non-null value for the slug field."""
        for field, model in self._get_fields(model_cls):
            if model is not None and field == slug_field:
                return model._default_manager.all()
        return model_cls._default_manager.all()

    def find_unique(self, model_instance: models.Model, field: models.Field[models.CharField], result_generator: str):
        queryset = self.get_queryset(model_instance.__class__, field)
        if model_instance.pk:
            # Exclude the current instance from the queryset to avoid
            # false positives when checking for uniqueness.
            queryset = queryset.exclude(pk=model_instance.pk)

        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)

        new = next(result_generator)
        kwargs[self.attname] = new

        while True:
            matching = queryset.filter(**kwargs)
            has_match = matching.exists()
            if new and not has_match:
                break

            new = next(result_generator)
            kwargs[self.attname] = new

        setattr(model_instance, self.attname, new)
        return new


class RandomCharField(UniqueFieldMixin, CharField):
    """A CharField that generates a random string when the model instance is saved."""

    def __init__(self, *args, lowercase: bool = False, uppercase: bool = False, include_digits: bool = True, include_alpha: bool = True, include_punctuation: bool = False, max_unique_tries: int | None = None, **kwargs):
        """
        Arguments:
            lowercase (bool): Whether to convert the generated string to lowercase. Default is False.
            uppercase (bool): Whether to convert the generated string to uppercase. Default is False.
            include_digits (bool): Whether to include digits in the generated string. Default is True.
            include_alpha (bool): Whether to include alphabetic characters in the generated string. Default is True.
            include_punctuation (bool): Whether to include punctuation characters in the generated string. Default is False.
            max_unique_tries (int, optional): The maximum number of attempts to generate a unique value before giving up. Default is 100 or the value of DJANGO_PLUS_MAX_UNIQUE_TRIES in settings.
        """
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        # Whether to convert the generated string to lowercase. Default is False.
        self.lowercase = lowercase
        self._check_bool(self.lowercase)

        # Whether to convert the generated string to uppercase. Default is False.
        self.uppercase = uppercase
        self._check_bool(self.uppercase)

        self.include_digits = include_digits
        self._check_bool(self.include_digits)

        self.include_alpha = include_alpha
        self._check_bool(self.include_alpha)

        self.max_unique_tries = max_unique_tries or MAX_UNIQUE_TRIES

        super().__init__(*args, **kwargs)

    def _check_bool(self, value: Any):
        if not isinstance(value, bool):
            raise ValueError(
                f"Expected a boolean value, got {type(value).__name__} instead.")

    def _random_generator(self, chars: str):
        for _ in range(self.max_unique_tries):
            yield ''.join(get_random_string(self.max_length, allowed_chars=chars))
        raise ValueError(
            f"Unable to generate a unique value after {self.max_unique_tries} attempts.")

    def internal_type(self):
        return 'CharField'

    def pre_save(self, model_instance, add):
        current_value = getattr(model_instance, self.attname)
        if current_value is not None and current_value != '':
            return current_value

        candidate_chars: str = ''
        if self.include_alpha:
            candidate_chars += string.ascii_letters

        if self.include_digits:
            candidate_chars += string.digits

        if self.include_punctuation:
            candidate_chars += string.punctuation

        if self.lowercase:
            candidate_chars = candidate_chars.lower()

        if self.uppercase:
            candidate_chars = candidate_chars.upper()

        result = self._random_generator(candidate_chars)

        field = model_instance._meta.get_field(self.attname)
        return self.find_unique(model_instance, field, result)


class CreationDateTimeField(models.DateTimeField):
    """A DateTimeField that automatically sets the value to the 
    current date and time when the model instance is created."""

    _is_creation_datetime = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault(
            'auto_now',
            True if not self._is_creation_datetime else False
        )
        kwargs.setdefault(
            'auto_now_add',
            True if self._is_creation_datetime else False
        )
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'DateTimeField'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.editable is not False:
            kwargs['editable'] = True

        if self.blank is not True:
            kwargs['blank'] = False

        if self.auto_now_add is not False:
            kwargs['auto_now_add'] = True

        return name, path, args, kwargs


class ModificationDateTimeField(CreationDateTimeField):
    """ A DateTimeField that automatically updates the value 
    to the current date and time whenever the model instance is saved. """

    _is_creation_datetime = False

    def get_internal_type(self):
        return 'DateTimeField'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now is not False:
            kwargs['auto_now'] = True
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if not getattr(model_instance, 'update_modified', True):
            return getattr(model_instance, self.attname)
        return super().pre_save(model_instance, add)
