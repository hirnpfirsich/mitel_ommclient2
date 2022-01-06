#!/usr/bin/env python3

from .session import Session
from . import messages

class OMMClient2:
    """
        High level wrapper for the OM Application XML Interface

        This class tries to provide functions for often used methods without the
        need of using the underlying messaging protocol

        :param host: Hostname or IP address of the OMM
        :param username: Username
        :param password: Password
        :param session: A :class:`mitel_ommclient2.session.Session` object

        Usage::

            >>> c = OMMClient2("omm.local", "admin", "admin")
            >>> c.ping()

        Use session for not implemented features::

            >>> r = s.session.request(mitel_ommclient2.messages.Ping())

        To get more contol over the connection handling, initialize
        :class:`mitel_ommclient2.session.Session` manually::

            >>> s = mitel_ommclient2.session.Session("omm.local", "admin", "admin", port=12345)
            >>> c = OMMClient2(session=s)
    """

    def __init__(self, host=None, username=None, password=None, session=None):
        if session is None:
            self.session = Session(host, username, password)
        else:
            self.session = session

    def get_account(self, id):
        """
            Get account

            :param id: User id
        """

        r = self.session.request(message.GetAccount(id))
        r.raise_on_error()

        return r.account[0]

    def ping(self):
        """
            Is OMM still there?

            Returns `True` when response is received.
        """

        r = self.session.request(messages.Ping())
        if r.errCode is None:
            return True
        return False
