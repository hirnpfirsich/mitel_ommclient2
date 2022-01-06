#!/usr/bin/env python3

import socket
import ssl


class Connection:
    """
        Establishes a connection to the OM Application XML Interface

        :param host: Hostname or IP address of OMM
        :param port: Port of the OM Application XML plain TCP port

        Usage::
            >>> c = Connection("omm.local")
            >>> c.connect()
            >>> c.send(request)
            >>> r = c.recv()
    """

    def __init__(self, host, port=12621):
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._recv_buffer = ""

    def connect(self):
        """
            Establishes the connection
        """

        self._socket.connect((self._host, self._port))

    def send(self, message):
        """
            Sends message string

            :param message: Message string
        """

        self._socket.send(message.encode("utf-8") + b"\0")

    def recv(self):
        """
            Returns one message

            Use multiple times to receive multiple messages
        """

        data = b""
        while True:
            new_data = self._socket.recv(65536)
            if new_data is not None:
                data += new_data
            else:
                break
        self._recv_buffer += data.decode("utf-8")

        if "\0" not in self._recv_buffer:
            # no new messages
            return None

        message, buffer = self._recv_buffer.split("\0", 1)
        self._recv_buffer = buffer

        return message

    def close(self):
        """
            Shout down connection
        """

        return self._socket.close()

    def __del__(self):
        self.close()


class SSLConnection(Connection):
    """
        Establishes a secure connection to the OM Application XML Interface

        :param host: Hostname or IP address of OMM
        :param port: Port of the OM Application XML ssl TCP port

        Usage:

        See :class:`Connection`
    """

    def __init__(self, host, port=12622):
        super().__init__(host, port)

        self._socket = ssl.wrap_socket(self._socket)
