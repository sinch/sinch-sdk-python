from typing import Literal, TypedDict, Union

from typing_extensions import NotRequired


class SayDict(TypedDict):
    text: str
    voice_name: str
    format: NotRequired[Union[Literal["TEXT", "SSML"], str]]


class SayMessageDict(TypedDict):
    type: Literal["SAY"]
    say: SayDict


class PlayDict(TypedDict):
    url: str


class PlayMessageDict(TypedDict):
    type: Literal["PLAY"]
    play: PlayDict


MessageDict = Union[SayMessageDict, PlayMessageDict]
