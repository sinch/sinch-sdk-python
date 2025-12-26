from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types import AgentType
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class Agent(BaseModelConfigurationResponse):
    display_name: Optional[StrictStr] = Field(
        default=None, description="Agent's display name"
    )
    type: Optional[AgentType] = None
    picture_url: Optional[StrictStr] = Field(
        default=None, description="The Agent's picture url."
    )
