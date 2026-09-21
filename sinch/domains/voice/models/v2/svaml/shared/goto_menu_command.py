from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class GotoMenuCommand(BaseModelConfiguration):
    command: Literal["gotoMenu"] = Field(
        default="gotoMenu",
        description="Switch execution to another menu within the current menu context.",
    )
    menu_name: StrictStr = Field(
        default=...,
        alias="menuName",
        description="Name of the target menu to execute next. Must match a key in menus.",
    )
