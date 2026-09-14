from typing import Literal, Optional, Union

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
    flags: Optional[
        Union[Literal["ONLY_PLAYING", "ALL_FROM_NOW_ON"], StrictStr]
    ] = Field(
        default=None,
        description="Controls how much of the sequence is stopped - only the currently playing message or all remaining queued messages.",
    )
