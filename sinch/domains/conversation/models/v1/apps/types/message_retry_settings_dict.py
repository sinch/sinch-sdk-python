from typing import TypedDict

from typing_extensions import NotRequired


class MessageRetrySettingsDict(TypedDict):
    retry_duration: NotRequired[int]
