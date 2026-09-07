from typing import List, Literal, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.message_dict import MessageDict
from sinch.domains.voice.models.v2.svaml.types.message_events_dict import (
    MessageEventsDict,
)


class MessagesCommandDict(TypedDict):
    command: Literal["messages"]
    messages_name: NotRequired[str]
    messages: List[MessageDict]
    events: NotRequired[MessageEventsDict]
