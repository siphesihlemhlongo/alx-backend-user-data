#!/usr/bin/env python3
"""
Session storage module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session class for storable and persistent
        sessions
    """
    def create_session(self, user_id: str = None) -> str:
        """ Creates session object
            Return:
                - id of session object
        """
        if not user_id or type(user_id) is not str:
            return None

        session = UserSession(**{"user_id": user_id})
        session.save()
        SessionDBAuth.user_id_by_session_id[session.session_id] =\
            session.user_id
        return session.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get user by session id
        """
        if not session_id or type(session_id) is not str:
            return None
        try:
            sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not sessions:
            return None
        session = sessions[0]
