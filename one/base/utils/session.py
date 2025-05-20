from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


def get_db_session_object(request):
    try:
        session_key = request.session.session_key
        db_session = Session.objects.get(pk=session_key)
    except (KeyError, Session.DoesNotExist):
        session_store = SessionStore()
        session_store.create()
        session_key = session_store.session_key
        request.session["sessionid"] = session_key
        db_session = Session.objects.get(session_key=session_key)
    return db_session
