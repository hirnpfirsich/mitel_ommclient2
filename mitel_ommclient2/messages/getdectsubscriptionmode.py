#!/usr/bin/env python3

from . import Request, Response, request_type, response_type


@request_type
class GetDECTSubscriptionMode(Request):
    pass


@response_type
class GetDECTSubscriptionModeResp(Response):
    FIELDS = {
        "mode": str,
    }
