#!/usr/bin/env python3

from time import sleep

from . import connection
from . import messages

class Session:
    """
        Synchronous API session handler

        :param host: Hostname or IP address of OMM
        :param username: Username
        :param password: Password
        :param port: Port
        :param ommsync: If True login as OMM-Sync client. Some operations in OMM-Sync mode might lead to destroy DECT paring.
        :param connection_class: One of :class:`mitel_ommclient2.connection.Connection` or :class:`mitel_ommclient2.connection.SSLConnection`

        Usage::
            >>> s = Session("omm.local", "admin", "admin")
            >>> s.request(mitel_ommclient2.messages.Ping())
    """

    def __init__(self, host, username, password, port=None, ommsync=False, connection_class=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ommsync = ommsync
        self.connection_class = connection_class
        if self.connection_class is None:
            self.connection_class = connection.Connection

        self._connection = None

        self._ensure_connection()

    def _wait_for_respose(self):
        """
            Wait until data got received and return message string
        """

        while True:
            r = self._connection.recv()
            if r is not None:
                return r
            sleep(0.1)

    def _ensure_connection(self):
        """
            Make sure we are connected and logged in
        """

        if self._connection is None:
            kwargs = {}
            if self.port is not None:
                kwargs["port"] = self.port
            self._connection = self.connection_class(self.host, **kwargs)

            self._connection.connect()

            # Login
            r = self.request(messages.Open(self.username, self.password, UserDeviceSyncClient=self.ommsync))

            r.raise_on_error()

    def request(self, request):
        """
            Sends a request and waits for response

            :param request: Request object

            Usage::
                >>> r = s.request(mitel_ommclient2.messages.Ping())
                >>> r.name
                'PingResp'
        """

        self._connection.send(request)

        return self._wait_for_respose()
