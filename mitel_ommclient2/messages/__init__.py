#!/usr/bin/env python3

from xml.dom.minidom import getDOMImplementation, parseString

from ..exceptions import exception_classes, OMResponseException


class Request:
    """
        Request message class

        :param name: Name of the message
        :param seq: Unique sequence number to associate responses

        Usage::
            >>> req = Request("Ping")
    """

    def __init__(self, name, seq=None):
        self.name = name
        self.attrs = {}
        self.childs = {}

        if seq is not None:
            self.attrs["seq"] = seq

    @property
    def seq(self):
        return self.attrs.get("seq")

    @seq.setter
    def seq(self, seq):
        self.attrs["seq"] = seq


class DictRequest(Request):
    """
        Create a message by dict attributes

        :param name: Name of the message
        :param attrs: Message attributes
        :param childs: Message children

        Usage::
            >>> req = DictRequest("Ping", {"timeStamp": 2342})
    """

    def __init__(self, name, attrs={}, childs={}):
        self.name = name
        self.attrs = attrs
        self.childs = childs


class Response:
    """
        Response message class

        :param name: Name of the message
        :param attrs: Message attributes
        :param childs: Message children
    """
    def __init__(self, name, attrs={}, childs={}):
        self.name = name
        self.attrs = attrs
        self.childs = childs

    def raise_on_error(self):
        """
            Raises an exception if the response contains an error.

            Usage::

                >>> try:
                >>>     r.raise_on_error()
                >>> except mitel_ommclient2.exceptions.EAuth as e:
                >>>     print("We don't care about authentication!")

            See children of :class:`mitel_ommclient2.exceptions.OMResponseException` for all possible exceptions.
        """

        if self.errCode is not None:
            raise exception_classes.get(self.errCode, OMResponseException)(response=self)

    @property
    def seq(self):
        return int(self.attrs.get("seq"))

    @property
    def errCode(self):
        return self.attrs.get("errCode")

    @property
    def info(self):
        return self.attrs.get("info")

    @property
    def bad(self):
        return self.attrs.get("bad")

    @property
    def maxLen(self):
        return self.attrs.get("maxLen")

from .getaccount import GetAccount, GetAccountResp
from .getppdev import GetPPDev, GetPPDevResp
from .open import Open, OpenResp
from .ping import Ping, PingResp

def construct(request):
    """
        Builds the XML message DOM and returns as string
    """
    impl = getDOMImplementation()
    message = impl.createDocument(None, request.name, None)
    root = message.documentElement

    for k, v in request.attrs.items():
        root.setAttribute(str(k), str(v))


    for k, v in request.childs.items():
        child = message.createElement(k)
        if v is not None:
            for c_k, c_v in v.items():
                child.setAttribute(str(c_k), str(c_v))
        root.appendChild(child)
    return root.toxml()

def _response_type_by_name(name):
    response_types = [
        GetAccountResp,
        GetPPDevResp,
        PingResp,
    ]

    response_types_dict = {r.__name__: r for r in response_types}

    return response_types_dict.get(name, Response)

def parse(message):
    message = parseString(message)
    root = message.documentElement

    name = root.tagName
    attrs = {}
    childs = {}

    for i in range(0, root.attributes.length):
        item = root.attributes.item(i)
        attrs[item.name] = item.value

    child = root.firstChild
    while child is not None:
        new_child = {}
        for i in range(0, child.attributes.length):
            item = child.attributes.item(i)
            new_child[item.name] = item.value

        childname = child.tagName
        if childname in childs:
            childs[childname].append(new_child)
        else:
            childs[childname] = [new_child]

        child = child.nextSibling


    return _response_type_by_name(name)(name, attrs, childs)
