#!/usr/bin/env python3

from . import Request, Response


class Open(Request):
    """
        Authenticate Message

        Needs to be the first message on a new connection.

        :param username: Username
        :param password: Password
        :param UserDeviceSyncClient: If True login as OMM-Sync client. Some operations in OMM-Sync mode might lead to destroy DECT paring.
    """
    def __init__(self, username, password, UserDeviceSyncClient=False, **kwargs):
        super().__init__("Open", **kwargs)

        self.attrs["username"] = username
        self.attrs["password"] = password
        if UserDeviceSyncClient:
            self.attrs["UserDeviceSyncClient"] = "true"

    @property
    def username(self):
        return self.attrs.get("username")

    @property
    def password(self):
        return self.attrs.get("password")

    @property
    def UserDeviceSyncClient(self):
        return self.attrs.get("UserDeviceSyncClient")

class OpenResp(Response):
    @property
    def protocolVersion(self):
        return self.attrs.get("protocolVersion")

    @property
    def minPPSwVersion1(self):
        return self.attrs.get("minPPSwVersion1")

    @property
    def minPPSwVersion2(self):
        return self.attrs.get("minPPSwVersion2")

    @property
    def ommStbState(self):
        return self.attrs.get("ommStbState")

    @property
    def publicKey(self):
        return self.attrs.get("publicKey")
