from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class AbstractTimeStampModel(models.Model):
    """Abstract model that provides created_at and updated_at fields.

    Attributes:
        created_at (DateTimeField): The date and time when the record was created.
        updated_at (DateTimeField): The date and time when the record was last updated.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class AbstractTitleDescriptionModel(models.Model):
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


class AbstractTitleSlugDescriptionModel(AbstractTitleDescriptionModel):
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


class AbstractUserProfile(AbstractTimeStampModel):
    """An abstract model that can be used to extend the default User model 
    with additional user profile information.
    
    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        company (CharField): The company or organization the user is associated with.
        job_title (CharField): The user's job title or position within the company.
        street_address (CharField): The user's street address.
        city (CharField): The city where the user resides.
        state (CharField): The state or province where the user resides.
        postal_code (CharField): The postal or ZIP code for the user's address.
        country (CharField): The country where the user resides.
        website (URLField): The user's personal or professional website.
        notes (TextField): Additional notes or information about the user.
        updated_on (DateTimeField): The timestamp when the profile was last updated.
        created_on (DateTimeField): The timestamp when the profile was created.
    """

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="The user's date of birth."
    )
    home_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The user's home phone number."
    )
    mobile_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The user's mobile phone number."
    )
    business_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The user's business phone number."
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The company or organization the user is associated with."
    )
    job_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The user's job title or position within the company."
    )
    street_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The user's street address."
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The city where the user resides."
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The state or province where the user resides."
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The postal or ZIP code for the user's address."
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The country where the user resides."
    )
    website = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="The user's personal or professional website."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or information about the user."
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
        indexes = (
            models.Index(
                name='user_profile_user_idx',
                fields=['user']
            ),
            models.Index(
                name='user_profile_updated_on_idx',
                fields=['street_address', 'city', 'state', 'postal_code', 'country']
            )
        )

    def __str__(self):
        """Return a string representation of the user profile."""
        return f"Profile of {self.user.username}"

    @cached_property
    def full_address(self):
        """Return the full address as a single string."""
        parts = [
            self.street_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(part for part in parts if part)

    @cached_property
    def contact_info(self):
        """Return a dictionary containing the user's contact information."""
        return {
            'home_phone': self.home_phone,
            'mobile_phone': self.mobile_phone,
            'business_phone': self.business_phone,
            'email': self.user.email,
            'website': self.website
        }

    @cached_property
    def profile_summary(self):
        """Return a summary of the user's profile information."""
        return {
            'full_name': self.user.get_full_name(),
            'company': self.company,
            'job_title': self.job_title,
            'address': self.full_address,
            'contact_info': self.contact_info,
            'notes': self.notes
        }

    @property
    def age(self) -> int | None:
        """Calculate and return the user's age based on their date of birth."""
        if self.date_of_birth is not None:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year
        return None
