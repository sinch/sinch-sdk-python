from typing import Literal, TypedDict


class GotoMenuCommandDict(TypedDict):
    command: Literal["gotoMenu"]
    menu_name: str
