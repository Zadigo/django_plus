import importlib

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, load_backend
from django.contrib.sessions.backends import db
from django.contrib.sessions.backends.base import VALID_KEY_CHARS
from django.core.management.base import BaseCommand
from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Get the user information for the provided session key. This is very helpful when trying to track down the person who experienced a site crash."

    def add_arguments(self, parser):
        parser.add_argument(
            "session_id", 
            nargs="+", 
            type=str, 
            help="The session key for which to retrieve user information. This is typically found in the session cookie of the user's browser."
        )

    @signalcommand
    def handle(self, *args, **options):
        session_id = options['session_id'][0]
        if not all(c in VALID_KEY_CHARS for c in session_id):
            self.stderr.write(self.style.ERROR("Invalid session key format."))
            return
        
        session_engine: db = importlib.import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore(session_id)
        data = store.load()

        self.stdout.write(self.style.SUCCESS(f"Session Data: {data}"))
        self.stdout.write(self.style.NOTICE(f"Session Expiry: {store.get_expiry_date()}"))

        uuid = data.get(SESSION_KEY)
        backend_path = data.get(BACKEND_SESSION_KEY, None)

        if backend_path is None:
            self.stderr.write(self.style.ERROR("No authentication backend associated with this session."))
            return

        if uuid is None:
            self.stderr.write(self.style.ERROR("No user associated with this session."))
            return

        backend_instance = load_backend(backend_path)
        user = backend_instance.get_user(uuid)
        if user is None:
            self.stderr.write(self.style.ERROR("No user found for the given user ID."))
            return

        message = f"""
        User ID: {uuid}
        Username: {user.get_username()}
        Email: {user.email}
        Is Staff: {user.is_staff}
        Is Superuser: {user.is_superuser}
        """
        
        self.stdout.write(message)
