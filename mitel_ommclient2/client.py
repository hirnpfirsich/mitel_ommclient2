#!/usr/bin/env python3

from .connection import Connection
from . import messages

class OMMClient2:
    """
        High level wrapper for the OM Application XML Interface

        This class tries to provide functions for often used methods without the
        need of using the underlying messaging protocol

        :param host: Hostname or IP address of the OMM
        :param username: Username
        :param password: Password
        :param port: Port where to access the API, if None, use default value
        :param ommsync: If True login as OMM-Sync client. Some operations in OMM-Sync mode might lead to destroy DECT paring.

        Usage::

            >>> c = OMMClient2("omm.local", "admin", "admin")
            >>> c.ping()

        Use request to send custom messages::

            >>> r = s.connection.request(mitel_ommclient2.messages.Ping())
    """

    def __init__(self, host, username, password, port=None, ommsync=False):
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._ommsync = ommsync

        # prepare connect arguments
        kwargs = {}
        if self._port is not None:
            kwargs["port"] = self._port

        # Connect
        self.connection = Connection(self._host, **kwargs)
        self.connection.connect()

        # Login
        r = self.connection.request(messages.Open(self._username, self._password, UserDeviceSyncClient=self._ommsync))
        r.raise_on_error()

    def get_account(self, id):
        """
            Get account

            :param id: User id
        """

        r = self.connection.request(messages.GetAccount(id))
        r.raise_on_error()
        if r.account is None:
            return None
        return r.account[0]

    def get_device(self, ppn):
        """
            Get PP device

            :param ppn: Device id
        """
        r = self.connection.request(messages.GetPPDev(ppn))
        r.raise_on_error()
        if r.pp is None:
            return None
        return r.pp[0]

    def ping(self):
        """
            Is OMM still there?

            Returns `True` when response is received.
        """

        r = self.connection.request(messages.Ping())
        if r.errCode is None:
            return True
        return False
