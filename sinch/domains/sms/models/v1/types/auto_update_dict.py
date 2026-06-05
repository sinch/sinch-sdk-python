from typing import TypedDict
from typing_extensions import NotRequired


class AddKeywordDict(TypedDict):
    first_word: str
    second_word: NotRequired[str]


class RemoveKeywordDict(TypedDict):
    first_word: str
    second_word: NotRequired[str]


class AutoUpdateDict(TypedDict):
    to: str
    add: NotRequired[AddKeywordDict]
    remove: NotRequired[RemoveKeywordDict]
