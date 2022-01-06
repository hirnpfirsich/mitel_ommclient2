#!/usr/bin/env python3

from . import Request, Response


class Open(Request):
    def __init__(self, username, password, **kwargs):
        super().__init__("Open", **kwargs)

        self.attrs["username"] = username
        self.attrs["password"] = password

    @property
    def username(self):
        return self.attrs.get("username")

    @property
    def password(self):
        return self.attrs.get("password")

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
