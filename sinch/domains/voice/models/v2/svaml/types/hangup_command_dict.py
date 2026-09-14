from typing import Literal, TypedDict

from typing_extensions import NotRequired


class HangupCommandDict(TypedDict):
    command: Literal["hangup"]
    call_name: NotRequired[str]
