from typing import TypedDict, Literal, Union, Annotated
from typing_extensions import NotRequired
from pydantic import Field


class VoiceConfigurationDictRTC(TypedDict):
    type: Literal["RTC"]
    app_id: NotRequired[str]


class VoiceConfigurationDictEST(TypedDict):
    type: Literal["EST"]
    trunk_id: NotRequired[str]


class VoiceConfigurationDictFAX(TypedDict):
    type: Literal["FAX"]
    service_id: NotRequired[str]


class VoiceConfigurationDictCustom(TypedDict):
    type: str


VoiceConfigurationDictType = Annotated[
    Union[VoiceConfigurationDictFAX, VoiceConfigurationDictRTC,
          VoiceConfigurationDictEST, VoiceConfigurationDictCustom],
    Field(discriminator="type")
]
