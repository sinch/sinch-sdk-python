from typing import Literal, TypedDict

from typing_extensions import NotRequired


class CustomEventCommandDict(TypedDict):
    command: Literal["customEvent"]
    custom_event_name: str
    url: str
    fallback_url: NotRequired[str]
