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
        :param connection_class: One of :class:`mitel_ommclient2.connection.Connection` or :class:`mitel_ommclient2.connection.SSLConnection`

        Usage::
            >>> s = Session("omm.local", "admin", "admin")
            >>> s.request(mitel_ommclient2.messages.Ping())
    """

    def __init__(self, host, username, password, port=None, connection_class=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
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
            r = self.connection.recv()
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
            self._connection.send(messages.Open(self.username, self.password))

            res = self._wait_for_respose()

            res.raise_on_error()

    def request(self, request):
        """
            Sends a request and waits for response

            :param request: Request object

            Usage::
                >>> r = s.request(mitel_ommclient2.messages.Ping())
                >>> r.name
                'PingResp'
        """

        message = messages.construct(request)
        self.connection.send(message)

        res = self._wait_for_respose()
        return messages.parse(res)
