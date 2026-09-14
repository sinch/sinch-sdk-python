from typing import Literal, TypedDict


class PauseCommandDict(TypedDict):
    command: Literal["pause"]
    duration_milliseconds: int
