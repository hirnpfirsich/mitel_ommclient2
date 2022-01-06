#!/usr/bin/env python3

from . import Request, Response


class GetAccount(Request):
    def __init__(self, id, maxRecords=None, **kwargs):
        super().__init__("GetAccount", **kwargs)

        self.attrs["id"] = id

        if maxRecords is not None:
            self.attrs["maxRecords"] = maxRecords

    @property
    def id(self):
        return self.attrs.get("id")

    @property
    def maxRecords(self):
        return self.attrs.get("maxRecords")


class GetAccountResp(Response):
    @property
    def account(self):
        return self.attrs.get("account")
