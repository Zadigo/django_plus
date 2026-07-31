import importlib
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.core.management import call_command
from django.test import TestCase


class TestUserForSession(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_with_invalid_characters(self):
        call_command('user_for_session', 'dummy_session_id', stderr=self.out)

        result = self.out.getvalue()
        self.assertIn("Invalid session key format.", result)

    @patch('django_plus.management.commands.user_for_session.db')
    def test_with_valid_session_id(self, mdb):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='testuser', password='testpassword')

        mdb.SessionStore.return_value.load.return_value = {
            SESSION_KEY: user.pk,
            BACKEND_SESSION_KEY: 'django.contrib.auth.backends.ModelBackend',
        }

        with patch.object(importlib, 'import_module', return_value=mdb):
            fake_session_id = 't07jdywyh7qhgtufo8heg6uuzt45vgpz'
            call_command('user_for_session', fake_session_id, stdout=self.out)

            result = self.out.getvalue()
            self.assertIn("Session Data:", result)
