#!/usr/bin/env python3

from . import Request, Response


class GetPPDev(Request):
    def __init__(self, ppn, maxRecords=None, **kwargs):
        super().__init__("GetPPDev", **kwargs)

        self.attrs["ppn"] = ppn

        if maxRecords is not None:
            self.attrs["maxRecords"] = maxRecords

    @property
    def ppn(self):
        return self.attrs.get("ppn")

    @property
    def maxRecords(self):
        return self.attrs.get("maxRecords")


class GetPPDevResp(Response):
    @property
    def pp(self):
        return self.childs.get("pp")
