from django.db import models

from django_plus.db.models import TimeStampModel


# TODO: A note for collect_notes command test
class TimestampedTestModel(TimeStampModel):
    book = models.CharField(max_length=100)
