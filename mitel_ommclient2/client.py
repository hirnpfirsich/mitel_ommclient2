#!/usr/bin/env python3

from .connection import Connection
from . import exceptions
from . import messages
from . import types

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
        m = messages.Open()
        m.username = self._username
        m.password = self._password
        m.UserDeviceSyncClient = self._ommsync
        r = self.connection.request(m)
        r.raise_on_error()

    def get_account(self, id):
        """
            Get account

            :param id: User id
        """

        m = messages.GetAccount()
        m.id = id
        r = self.connection.request(m)
        r.raise_on_error()
        if r.childs.account is None:
            return None
        return r.childs.account[0]

    def get_device(self, ppn):
        """
            Get PP device

            :param ppn: Device id
        """

        m = messages.GetPPDev()
        m.ppn = ppn
        r = self.connection.request(m)
        r.raise_on_error()
        if r.childs.pp is None:
            return None
        return r.childs.pp[0]

    def get_devices(self):
        """
            Get all PP devices
        """
        next_ppn = 0
        while True:
            m = messages.GetPPDev()
            m.ppn = next_ppn
            m.maxRecords = 20
            r = self.connection.request(m)
            try:
                r.raise_on_error()
            except exceptions.ENoEnt:
                # No more devices to fetch
                break

            # Output all found devices
            for pp in r.childs.pp:
                yield pp

            # Determine next possible ppn
            next_ppn = int(pp.ppn) + 1

    def get_user(self, uid):
        """
            Get PP user

            :param uid: User id
        """
        m = messages.GetPPUser()
        m.uid = uid
        r = self.connection.request(m)
        r.raise_on_error()
        if r.childs.user is None:
            return None
        return r.childs.user[0]

    def get_users(self):
        """
            Get all PP users
        """
        next_uid = 0
        while True:
            m = messages.GetPPUser()
            m.uid = next_uid
            m.maxRecords = 20
            r = self.connection.request(m)
            try:
                r.raise_on_error()
            except exceptions.ENoEnt:
                # No more devices to fetch
                break

            # Output all found devices
            for user in r.childs.user:
                yield user

            # Determine next possible ppn
            next_uid = int(user.uid) + 1

    def ping(self):
        """
            Is OMM still there?

            Returns `True` when response is received.
        """

        r = self.connection.request(messages.Ping())
        if r.errCode is None:
            return True
        return False

    def set_user_name(self, uid, name):
        """
            Set PP user name

            :param uid: User id
            :param name: User name
        """
        t = types.PPUserType()
        t.uid = uid
        t.name = name
        m = messages.SetPPUser()
        m.childs.user = [t]
        r = self.connection.request(m)
        r.raise_on_error()
        if r.childs.user is None:
            return None
        return r.childs.user[0]

    def set_user_num(self, uid, num):
        """
            Set PP user number

            :param uid: User id
            :param num: User number
        """
        t = types.PPUserType()
        t.uid = uid
        t.num = num
        m = messages.SetPPUser()
        m.childs.user = [t]
        r = self.connection.request(m)

        r.raise_on_error()
        if r.childs.user is None:
            return None
        return r.childs.user[0]
