from typing import Dict, Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.menu_item import MenuItem


class MenuCommand(BaseModelConfiguration):
    command: Literal["menu"] = Field(
        default="menu",
        description="Executes menu-based input collection using the configured menu definitions.",
    )
    start_menu: StrictStr = Field(
        default=...,
        alias="startMenu",
        description="Name of the menu to execute first. Must match a key in menus.",
    )
    menus: Dict[StrictStr, MenuItem] = Field(
        default=...,
        description="Map of menu definitions keyed by menu name.",
    )
