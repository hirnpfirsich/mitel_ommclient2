#!/usr/bin/env python3

from . import Request, Response, request_type, response_type


@request_type
class GetAccount(Request):
    FIELDS = {
        "id": int,
        "maxRecords": int,
    }


@response_type
class GetAccountResp(Response):
    CHILDS = {
        "account": None,
    }
