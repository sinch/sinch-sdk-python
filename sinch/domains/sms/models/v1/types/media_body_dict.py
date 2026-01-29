from typing import TypedDict
from typing_extensions import NotRequired


class MediaBodyDict(TypedDict):
    url: str
    subject: NotRequired[str]
    message: NotRequired[str]
