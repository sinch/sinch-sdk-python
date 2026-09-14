from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired


class StopMessagesCommandDict(TypedDict):
    command: Literal["stopMessages"]
    messages_name: str
    flags: NotRequired[Union[Literal["ONLY_PLAYING", "ALL_FROM_NOW_ON"], str]]
