from django_plus.db.models import TimeStampModel


class TimestampedTestModel(TimeStampModel):
    class Meta:
        app_label = 'django_plus'
