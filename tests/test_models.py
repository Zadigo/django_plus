from django.test import TestCase
from tests.testapp.models import TimestampedTestModel


class TestTimeStampModel(TestCase):
    def test_implementation(self):
        instance = TimestampedTestModel.objects.create()
        print(instance)
