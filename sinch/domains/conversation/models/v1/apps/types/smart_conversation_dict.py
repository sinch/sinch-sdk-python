from typing import TypedDict

from typing_extensions import NotRequired


class SmartConversationDict(TypedDict):
    enabled: NotRequired[bool]
