from typing import TypedDict, Literal
from typing_extensions import NotRequired


class VoiceConfigurationESTDict(TypedDict):
    type: Literal["EST"]
    trunk_id: NotRequired[str]
