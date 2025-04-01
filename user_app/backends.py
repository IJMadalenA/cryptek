import datetime

from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore as DBStore


class SessionStore(DBStore):
    """
    SessionStore is a specialized session management class designed to handle session-specific
    data and operations while extending the functionality of a database-backed session store.

    It provides methods for manipulating and maintaining session details, including metadata like
    user agent, IP address, and user ID. The class ensures proper initialization, retrieval, and
    saving of session-related data into the database, enabling effective session persistence and
    tracking. It also overrides certain core session operations to support enhanced metadata
    management.

    Attributes:
        user_agent (str): User agent string associated with the session, truncated to a maximum
            length of 200 characters.
        ip (str): IP address of the client initiating the session.
        referer (str): URL of the referring page for this session, truncated to a maximum length of
            200 characters.
        accept_language (str): Information about the client's preferred languages, truncated to a
            maximum length of 200 characters.
        request_path (str): Request path of the client for this session.
        timestamp (datetime.datetime): Timestamp of the session's creation or update. Defaults to
            the current time if not provided.
        user_id (int or None): The ID of the user associated with the session, if applicable.
    """

    def __init__(
        self,
        session_key=None,
        user_agent=None,
        ip=None,
        referer=None,
        accept_language=None,
        request_path=None,
        timestamp=None,
    ):
        super().__init__(session_key)
        # Truncate user_agent string to max_length of the CharField
        self.user_agent = user_agent[:200] if user_agent else user_agent
        self.ip = ip
        self.referer = referer[:200] if referer else referer
        self.accept_language = accept_language[:200] if accept_language else accept_language
        self.request_path = request_path
        self.timestamp = timestamp if timestamp else datetime.datetime.now()
        self.user_id = None

    # Used by superclass to get self.model, which is used elsewhere
    @classmethod
    def get_model_class(cls):
        from user_app.models.session import Session

        return Session

    def __setitem__(self, key, value):
        if key == auth.SESSION_KEY:
            self.user_id = value
        super().__setitem__(key, value)

    # Used in DBStore.load()
    def _get_session_from_db(self):
        s = super()._get_session_from_db()
        if s is not None:
            self.user_id = s.user_id
            # do not overwrite user_agent/ip, as those might have been updated
            if self.user_agent != s.user_agent or self.ip != s.ip:
                self.modified = True
        return s

    def create(self):
        super().create()
        self._session_cache = {}

    # Used in DBStore.save()
    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
            user_agent=self.user_agent,
            user_id=self.user_id,
            ip=self.ip,
            referer=self.referer,
            accept_language=self.accept_language,
            request_path=self.request_path,
            timestamp=self.timestamp,
        )

    def clear(self):
        super().clear()
        self.user_id = None
