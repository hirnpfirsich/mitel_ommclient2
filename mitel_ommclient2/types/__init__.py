#!/usr/bin/env python3

class ChildType:
    """
        Base type class

        :param name: Name of the message
        :param attrs: Message attributes
        :param childs: Message children
    """

    FIELDS = {}


    def __init__(self, attrs={}):
        self._attrs = {}

        for k, v in attrs.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        if name in self.FIELDS.keys():
            return self._attrs.get(name)
        else:
            raise AttributeError()

    def __setattr__(self, name, value):
        if name in self.FIELDS.keys():
            if self.FIELDS[name] is not None and type(value) != self.FIELDS[name]:
                raise TypeError()
            self._attrs[name] = value
        else:
            object.__setattr__(self, name, value)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self._attrs))

def cast_dict_to_childtype(t, d):
    for k, v in d.items():
        if k in t.FIELDS.keys():
            if t.FIELDS[k] is not None and type(v) != t.FIELDS[k]:
                d[k] = t.FIELDS[k](v)
        else:
            raise KeyError()

    return t(d)

class PPUserType(ChildType):
    FIELDS = {
        "uid": int,
        "timeStamp": int,
        "relType": None, #PPRelTypeType,
        "ppn": int,
        "name": str,
        "num": str,
        "hierarchy1": str,
        "hierarchy2": str,
        "addId": str,
        "pin": str,
        "sipAuthId": str,
        "sipPw": str,
        "sosNum": str,
        "voiceboxNum": str,
        "manDownNum": str,
        "forwardStateCall": None, #ForwardStateType,
        "forwardTime": int,
        "forwardDest": str,
        "langPP": None, #LanguageType,
        "holdRingBackTime": int,
        "autoAnswer": str,
        "microphoneMute": str,
        "warningTone": str,
        "allowBargeIn": str,
        "callWaitingDisabled": bool,
        "external": bool,
        "trackingActive": bool,
        "locatable": bool,
        "BTlocatable": bool,
        "BTsensitivity": str,
        "locRight": bool,
        "msgRight": bool,
        "sendVcardRight": bool,
        "recvVcardRight": bool,
        "keepLocalPB": bool,
        "vip": bool,
        "sipRegisterCheck": bool,
        "allowVideoStream": bool,
        "conferenceServerType": str,
        "conferenceServerURI": str,
        "monitoringMode": str,
        "CUS": None, #MonitoringStateType,
        "HAS": None, #MonitoringStateType,
        "HSS": None, #MonitoringStateType,
        "HRS": None, #MonitoringStateType,
        "HCS": None, #MonitoringStateType,
        "SRS": None, #MonitoringStateType,
        "SCS": None, #MonitoringStateType,
        "CDS": None, #MonitoringStateType,
        "HBS": None, #MonitoringStateType,
        "BTS": None, #MonitoringStateType,
        "SWS": None, #MonitoringStateType,
        "credentialPw": str,
        "configurationDataLoaded": bool,
        "ppData": str,
        "ppProfileId": int,
        "fixedSipPort": int,
        "calculatedSipPort": int,
        # undocumented
        "uidSec": int,
        "permanent": bool,
        "lang": None,
        "forwardState": None,
        "autoLogoutOnCharge": bool,
        "hotDeskingSupport": bool,
        "authenticateLogout": bool,
        "useSIPUserName": None,
        "useSIPUserAuthentication": None,
        "serviceUserName": None,
        "serviceAuthName": None,
        "serviceAuthPassword": None,
        "keyLockEnable": None,
        "keyLockPin": None,
        "keyLockTime": None,
    }
