#!/usr/bin/env python3

from . import Request, Response


class GetPPUser(Request):
    def __init__(self, uid, maxRecords=None, **kwargs):
        super().__init__("GetPPUser", **kwargs)

        self.attrs["uid"] = uid

        if maxRecords is not None:
            self.attrs["maxRecords"] = maxRecords

    @property
    def ppn(self):
        return self.attrs.get("ppn")

    @property
    def maxRecords(self):
        return self.attrs.get("maxRecords")


class GetPPUserResp(Response):
    @property
    def user(self):
        return self.childs.get("user")
