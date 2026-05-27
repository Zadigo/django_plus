import pathlib
from django.test import TestCase
from unittest.mock import Mock, patch
from django.core.management import call_command, CommandError
from django.test import override_settings


TEST_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()


@patch('django_plus.management.commands.sync_s3.HAS_BOTO', True)
class TestSyncS3Exceptionss(TestCase):
    def test_raises_exception_when_boto_not_installed(self):
        with patch('django_plus.management.commands.sync_s3.HAS_BOTO', False):
            with self.assertRaises(CommandError):
                call_command('sync_s3')

    def test_raises_exception_when_no_access_keys(self):
        with self.settings(AWS_S3_ACCESS_KEY_ID=None, AWS_S3_SECRET_ACCESS_KEY=None):
            with self.assertRaises(CommandError):
                call_command('sync_s3')

    def test_raises_exception_when_no_bucket_name(self):
        with self.settings(AWS_S3_ACCESS_KEY_ID='secret1', AWS_S3_SECRET_ACCESS_KEY='secret2', AWS_STORAGE_BUCKET_NAME=None):
            with self.assertRaises(CommandError):
                call_command('sync_s3')

    def test_raises_exception_when_no_media_root(self):
        with self.settings(AWS_S3_ACCESS_KEY_ID='secret1', AWS_S3_SECRET_ACCESS_KEY='secret2', AWS_STORAGE_BUCKET_NAME='bucket', MEDIA_ROOT=None):
            with self.assertRaises(CommandError):
                call_command('sync_s3')


@override_settings(AWS_S3_ACCESS_KEY_ID='secret1', AWS_S3_SECRET_ACCESS_KEY='secret2', AWS_STORAGE_BUCKET_NAME='bucket', MEDIA_ROOT=TEST_DIR.joinpath('media'))
@patch('django_plus.management.commands.sync_s3.boto3', create=True)
@patch('django_plus.management.commands.sync_s3.HAS_BOTO', Mock(side_effect=True))
class TestSyncS3Command(TestCase):
    def setUp(self):
        # This sequence will be used to create a test media directory with some files
        # in it in order to test the file discovery and upload process of the command.
        self.test_dir = TEST_DIR
        self.media_dir = self.test_dir.joinpath('media')
        if not self.media_dir.is_dir() and not self.media_dir.exists():
            # self.media_dir.rmdir()

            self.media_dir.mkdir(exist_ok=True)

            test_dirs = ['dir1', 'dir2', 'dir3', 'dir4/subdir1']
            for d in test_dirs:
                path = self.media_dir.joinpath(d)
                path.mkdir(parents=True, exist_ok=True)
                for i in range(2):
                    file_path = path.joinpath(f'file{i}.txt')
                    file_path.touch()

    # def tearDown(self):
    #     # Clean up the test media directory after the tests are done.
    #     for item in self.media_dir.glob('**/*'):
    #         if item.is_file():
    #             item.unlink()
    #         elif item.is_dir():
    #             item.rmdir()
    #     self.media_dir.rmdir()

    def test_sync_s3_command(self, mboto3):
        # Mock the S3 client and its methods
        # mock_s3_client = Mock()
        # mboto3.client.return_value = mock_s3_client

        # Call the command
        call_command('sync_s3')

        # Check that the S3 client was created with the correct parameters
        # mboto3.client.assert_called_with(
        #     's3',
        #     aws_access_key_id='secret1',
        #     aws_secret_access_key='secret2',
        #     region_name=None
        # )

        # # Check that the upload_fileobj method was called for each file in the media directory
        # expected_calls = []
        # for path in self.media_dir.glob('**/*'):
        #     if path.is_file():
        #         expected_calls.append(((str(path), 'bucket', str(path.relative_to(self.media_dir))),))
        # mock_s3_client.upload_fileobj.assert_has_calls(expected_calls, any_order=True)
