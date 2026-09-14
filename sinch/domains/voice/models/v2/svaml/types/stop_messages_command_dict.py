from typing import Literal, TypedDict


class StopMessagesCommandDict(TypedDict):
    command: Literal["stopMessages"]
    messages_name: str
