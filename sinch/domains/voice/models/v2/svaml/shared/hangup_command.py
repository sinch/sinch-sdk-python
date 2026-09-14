from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class HangupCommand(BaseModelConfiguration):
    command: Literal["hangup"] = Field(
        default="hangup", description="Hangup call"
    )
    call_name: Optional[StrictStr] = Field(
        default=None,
        alias="callName",
        description="Name of the call leg to end, as set by `callName` in the `dial` command.\n\nIf omitted, the current call leg is ended.",
    )
