#!/usr/bin/env python3

import queue
import select
import socket
import ssl
import threading

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

        self._received_messages = queue.Queue()

        self._close = False

    def connect(self):
        """
            Establishes the connection
        """

        self._socket.connect((self._host, self._port))
        self._socket.setblocking(False)

        threading.Thread(target=self._receive_loop, daemon=True).start()

    def send(self, message):
        """
            Sends message string

            :param message: Message string
        """

        self._socket.send(message.encode("utf-8") + b"\0")

    def _receive_loop(self):
        recv_buffer = b""

        while not self._close:
            if select.select([self._socket], [], []) != ([], [], []):
                # wait for data availiable
                while True:
                    # fill buffer with one message
                    data = self._socket.recv(1024)

                    if not data:
                        break

                    recv_buffer += data

                    if b"\0" in recv_buffer:
                        break


                if b"\0" not in recv_buffer:
                    # no new messages
                    break

                message, buffer = recv_buffer.split(b"\0", 1)
                recv_buffer = buffer

                self._received_messages.put(message)

    def recv(self):
        """
            Returns one message

            Use multiple times to receive multiple messages
        """

        if self._received_messages.empty():
            return None

        return self._received_messages.get().decode("utf-8")

    def close(self):
        """
            Shut down connection
        """

        self._close = True
        return self._socket.close()

    def __del__(self):
        self.close()


class SSLConnection(Connection):
    """
        Establishes a secure connection to the OM Application XML Interface

        Please not that this class might be useless on your system since new
        versions of OpenSSL don't ship with TLVv1.2 or lower anymore which are
        the protocols supported by OMM.

        :param host: Hostname or IP address of OMM
        :param port: Port of the OM Application XML ssl TCP port

        Usage:

        See :class:`Connection`
    """

    def __init__(self, host, port=12622):
        super().__init__(host, port)

        self._socket = ssl.wrap_socket(self._socket)
