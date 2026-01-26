from typing import TypedDict
from typing_extensions import NotRequired


class MediaPropertiesDict(TypedDict):
    url: str
    thumbnail_url: NotRequired[str]
    filename_override: NotRequired[str]
