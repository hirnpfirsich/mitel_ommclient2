#!/usr/bin/env python3

from . import Request, Response


class Ping(Request):
    def __init__(self, timeStamp=None, **kwargs):
        super().__init__("Ping", **kwargs)

        if timeStamp is not None:
            self.attrs["timeStamp"] = timeStamp

    @property
    def timeStamp(self):
        return self.attrs.get("timeStamp")

class PingResp(Response):
    @property
    def timeStamp(self):
        return self.attrs.get("timeStamp")
