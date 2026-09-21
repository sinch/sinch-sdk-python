from typing import List, Literal, TypedDict, Union

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.call_header_dict import CallHeaderDict


class SipDetailsDict(TypedDict):
    endpoint: str
    transport: NotRequired[Union[Literal["UDP", "TCP", "TLS"], str]]
    call_headers: NotRequired[List[CallHeaderDict]]


class SipDict(TypedDict):
    type: Literal["SIP"]
    sip: SipDetailsDict
