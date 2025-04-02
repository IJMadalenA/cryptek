from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware as DjangoSessionMiddleware


class SessionMiddleware(DjangoSessionMiddleware):
    """
    Middleware that provides ip and user_agent to the session store.
    """

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = self.SessionStore(
            # ip=request.META.get("REMOTE_ADDR", ""),
            # user_agent=request.META.get("HTTP_USER_AGENT", ""),
            # referer=request.META.get("HTTP_REFERER", ""),
            # accept_language=request.META.get("HTTP_ACCEPT_LANGUAGE", ""),
            # request_path=request.path,
            # timestamp=datetime.now(),
            session_key=session_key,
        )
