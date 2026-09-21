from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class MenuInput(BaseModelConfiguration):
    menu_name: StrictStr = Field(
        default=...,
        alias="menuName",
        description="The name of the menu that triggered this sinch event.",
    )
    input: StrictStr = Field(
        default=...,
        description="The input sequence gathered from the user by the menu.",
    )
