from typing import Literal, TypedDict

from typing_extensions import NotRequired


class SipFromDetailsDict(TypedDict):
    endpoint: str
    display_name: NotRequired[str]


class SipFromDict(TypedDict):
    type: Literal["SIP"]
    sip: SipFromDetailsDict
