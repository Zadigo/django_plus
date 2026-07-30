import pathlib

from django.core.management import call_command
from django.test import TestCase, override_settings

TEST_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()


@override_settings(MEDIA_ROOT=TEST_DIR.joinpath('media'))
class CheckMediaRootCommandTestCase(TestCase):
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

    def test_basic_implementation(self):
        call_command('check_media_root')
