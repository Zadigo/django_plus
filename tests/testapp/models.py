from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_plus.db.models import (
    AbstractTimeStampModel,
    AbstractTitleDescriptionModel,
    AbstractTitleSlugDescriptionModel,
    AbstractUserProfile,
)


# TODO: Note for testing collect_notes command
class Book(AbstractTitleDescriptionModel):
    book = models.CharField(max_length=100)

    def __str__(self):
        return self.book


class Journal(AbstractTitleSlugDescriptionModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(AbstractTimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(AbstractUserProfile):
    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=Book)
def pre_save_receiver(sender, instance, **kwargs):
    # Signal for testing list_signals command
    pass
