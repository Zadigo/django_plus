import importlib
import time
from io import StringIO
from unittest.mock import Mock, patch

from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.core.management import call_command
from django.test import TestCase


class TestUserForSession(TestCase):
    def setUp(self):
        self.out = StringIO()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='testuser', password='testpassword')
        self.fake_session_id = 't07jdywyh7qhgtufo8heg6uuzt45vgpz'

    def test_with_invalid_characters(self):
        call_command('user_for_session', 'dummy_session_id', stderr=self.out)

        result = self.out.getvalue()
        self.assertIn("Invalid session key format.", result)

    @patch('django_plus.management.commands.user_for_session.db')
    def test_with_valid_session_id(self, mdb: Mock):
        mdb.SessionStore.return_value.load.return_value = {
            SESSION_KEY: self.user.pk,
            BACKEND_SESSION_KEY: 'django.contrib.auth.backends.ModelBackend',
        }

        with patch.object(importlib, 'import_module', return_value=mdb):
            call_command('user_for_session', self.fake_session_id, stdout=self.out)

            result = self.out.getvalue()

            self.assertIn("Session Data:", result)

            mdb.SessionStore.return_value.load.assert_called_once()

    @patch('django_plus.management.commands.user_for_session.db')
    def test_no_backend_path(self, mdb: Mock):
        mdb.SessionStore.return_value.load.return_value = {
            SESSION_KEY: self.user.pk,
            BACKEND_SESSION_KEY: None
        }

        with patch.object(importlib, 'import_module', return_value=mdb):
            call_command('user_for_session', self.fake_session_id, stderr=self.out)

            result = self.out.getvalue()
            self.assertIn("No authentication backend associated with this session.", result)

    @patch('django_plus.management.commands.user_for_session.db')
    def test_no_user_id(self, mdb: Mock):
        mdb.SessionStore.return_value.load.return_value = {
            SESSION_KEY: None,
            BACKEND_SESSION_KEY: 'django.contrib.auth.backends.ModelBackend'
        }

        with patch.object(importlib, 'import_module', return_value=mdb):
            call_command('user_for_session', self.fake_session_id, stderr=self.out)

            result = self.out.getvalue()
            self.assertIn("No user associated with this session.", result)

    @patch('django.contrib.auth.load_backend')
    def test_no_user_found(self, mload_backend: Mock):
        time.sleep(2)  # Ensure the session has a unique timestamp for testing
        
        mload_backend.return_value.get_user.return_value = None

        with patch('django_plus.management.commands.user_for_session.db') as mdb:
            mdb.SessionStore.return_value.load.return_value = {
                SESSION_KEY: self.user.pk,
                BACKEND_SESSION_KEY: 'django.contrib.auth.backends.ModelBackend'
            }

            with patch.object(importlib, 'import_module', return_value=mdb):
                call_command('user_for_session', self.fake_session_id, stderr=self.out)

                result = self.out.getvalue()
                self.assertIn("No user found for the given user ID.", result)
