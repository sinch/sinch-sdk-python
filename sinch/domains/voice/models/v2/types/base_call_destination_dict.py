from typing import Literal, TypedDict, Union

from sinch.domains.voice.models.v2.types.phone_dict import PhoneDict


class BaseEndpointDetailsDict(TypedDict):
    endpoint: str


class BaseSipDict(TypedDict):
    type: Literal["SIP"]
    sip: BaseEndpointDetailsDict


class BaseStreamDict(TypedDict):
    type: Literal["STREAM"]
    stream: BaseEndpointDetailsDict


BaseCallDestinationDict = Union[PhoneDict, BaseSipDict, BaseStreamDict]
