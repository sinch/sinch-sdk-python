from typing import TypedDict, Literal
from typing_extensions import NotRequired


class VoiceConfigurationRTCDict(TypedDict):
    type: Literal["RTC"]
    app_id: NotRequired[str]
