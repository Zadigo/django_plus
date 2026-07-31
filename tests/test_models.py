import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from tests.testapp.models import Author, Book, Journal, UserProfile


@pytest.mark.unit
@pytest.mark.django_db
@pytest.mark.parametrize("name",["John Doe", "Jane Smith"])
def test_timestamp_model(name):
    author = Author.objects.create(name=name)
    assert author.created_at is not None
    assert author.updated_at is not None


@pytest.mark.unit
@pytest.mark.django_db
@pytest.mark.parametrize("name",["Science Journal", "Tech Journal"])
def test_journal_model(name):
    journal = Journal.objects.create(name=name)
    assert journal.name is not None


@pytest.mark.unit
@pytest.mark.django_db
def test_book_model():
    book = Book.objects.create(
        book="Science Journal",
        title="Science Journal Title",
        description="A journal about science."
    )
    assert book.title is not None


@pytest.mark.unit
@pytest.mark.django_db
def test_userprofile_model():
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="johndoe",
        email='johndoe@example.com',
        password='securepassword'
    )

    userprofile = UserProfile.objects.get(user=user)
    assert userprofile is not None

    userprofile.street_address = "123 Main St"
    userprofile.city = "Anytown"
    userprofile.state = "CA"
    userprofile.postal_code = "12345"
    userprofile.country = "USA"

    dob = datetime.date(1990, 1, 1)
    userprofile.date_of_birth = dob

    userprofile.save()

    # Test properties
    assert userprofile.full_address == "123 Main St, Anytown, CA, 12345, USA"

    assert userprofile.age is not None
    assert isinstance(userprofile.age, int)
    assert userprofile.age == (timezone.now().date().year - dob.year)

    assert isinstance(userprofile.contact_info, dict)
    assert isinstance(userprofile.profile_summary, dict)

    userprofile.date_of_birth = None
    userprofile.save()

    assert userprofile.age is None

    # result = userprofile.__str__()
    # assert result == f"Profile of {user.username}"
