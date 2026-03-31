from typing import TypedDict, Literal
from typing_extensions import NotRequired


class VoiceConfigurationFAXDict(TypedDict):
    type: Literal["FAX"]
    service_id: NotRequired[str]
