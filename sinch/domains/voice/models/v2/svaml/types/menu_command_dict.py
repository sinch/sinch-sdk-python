from typing import Dict, Literal, TypedDict

from sinch.domains.voice.models.v2.svaml.types.menu_item_dict import (
    MenuItemDict,
)


class MenuCommandDict(TypedDict):
    command: Literal["menu"]
    start_menu: str
    menus: Dict[str, MenuItemDict]
