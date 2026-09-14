from typing import Literal, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.message import Message
from sinch.domains.voice.models.v2.svaml.shared.message_events import (
    MessageEvents,
)


class MessagesCommand(BaseModelConfiguration):
    command: Literal["messages"] = Field(
        default="messages",
        description="Command to play a message on the channel",
    )
    messages_name: Optional[StrictStr] = Field(
        default=None,
        alias="messagesName",
        description="Name of the message for identification and reference within the call session.\n\nThis name is used to uniquely identify the message and must be unique within the current call session.\nThis name can be referenced in other commands (e.g., `stopMessages`) to control this specific message.",
    )
    messages: conlist(Message) = Field(
        default=...,
        description="Ordered list of messages to play. Must contain between 1 and 10 messages.",
    )
    events: Optional[MessageEvents] = Field(default=None)
