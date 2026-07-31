from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_plus.db.models import (
    AbstractTimeStampModel,
    AbstractTitleDescriptionModel,
    AbstractTitleSlugDescriptionModel,
    AbstractUserProfile,
)

USER_MODEL = get_user_model()


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


@receiver(post_save, sender=USER_MODEL)
def post_save_receiver(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
