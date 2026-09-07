from typing import TypedDict

from typing_extensions import NotRequired


class CallHeaderDict(TypedDict):
    key: str
    value: NotRequired[str]
