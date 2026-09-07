from typing import TypedDict

from typing_extensions import NotRequired


class TranscriptionOptionsDict(TypedDict):
    is_enabled: bool
    locale: NotRequired[str]
