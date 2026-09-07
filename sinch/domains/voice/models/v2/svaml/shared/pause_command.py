from typing import Literal

from pydantic import Field, StrictInt

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class PauseCommand(BaseModelConfiguration):
    command: Literal["pause"] = Field(
        default="pause", description="Pause execution."
    )
    duration_milliseconds: StrictInt = Field(
        default=...,
        alias="durationMilliseconds",
        description="Duration of the pause in milliseconds.",
    )
