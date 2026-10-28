from pydantic import Field

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.shared.agent import Agent


class AgentJoinedEvent(BaseModelConfiguration):
    agent: Agent = Field(
        default=...,
        description="Represents an agent that is involved in a conversation.",
    )
