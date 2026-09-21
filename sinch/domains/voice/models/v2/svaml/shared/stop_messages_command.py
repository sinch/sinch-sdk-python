from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StopMessagesCommand(BaseModelConfiguration):
    command: Literal["stopMessages"] = Field(
        default="stopMessages", description="Command to stop playing messages"
    )
    messages_name: StrictStr = Field(
        default=...,
        alias="messagesName",
        description="Name of the message sequence to stop, as set by `messagesName` in the `messages` command.",
    )
