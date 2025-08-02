#!/usr/bin/env python3

from . import Request, Response, request_type, response_type


@request_type
class SetDECTSubscriptionMode(Request):
    FIELDS = {
        "mode": str,
        "timeout": int,
    }


@response_type
class SetDECTSubscriptionModeResp(Response):
    pass
