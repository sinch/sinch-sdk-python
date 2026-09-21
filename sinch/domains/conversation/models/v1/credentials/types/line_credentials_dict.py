from typing import TypedDict
from typing_extensions import NotRequired


class LineCredentialsDict(TypedDict):
    token: str
    secret: str
    is_default: NotRequired[bool]
