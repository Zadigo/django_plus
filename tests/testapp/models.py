from django_plus.db.models import TimeStampModel


# TODO: A note for collect_notes command test
class TimestampedTestModel(TimeStampModel):
    class Meta:
        app_label = 'tests.testapp'
