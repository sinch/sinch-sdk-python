from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.agent_type import (
    AgentType,
)


class AgentDict(TypedDict):
    display_name: NotRequired[str]
    type: NotRequired[AgentType]
    picture_url: NotRequired[str]
