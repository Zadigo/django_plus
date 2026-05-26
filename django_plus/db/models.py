from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    """Abstract model that provides created_at and updated_at fields.

    Attributes:
        created_at (DateTimeField): The date and time when the record was created.
        updated_at (DateTimeField): The date and time when the record was last updated.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TitleDescriptionModel(models.Model):
    """Abstract model that provides title and description fields.

    Attributes:
        title (CharField): The title of the record.
        description (TextField): The description of the record.
    """

    title = models.CharField(
        _('Title'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class TitleSlugDescriptionModel(TitleDescriptionModel):
    """Abstract model that provides title, slug, and description fields.

    Attributes:
        slug (SlugField): The slug of the record, used for URL-friendly representations.
    """

    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        unique=True
    )

    class Meta:
        abstract = True
