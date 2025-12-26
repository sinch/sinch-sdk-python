from typing import Any, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class FlowActionPayloadInternal(BaseModelConfigurationResponse):
    screen: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the screen displayed first. This must be an entry screen.",
    )
    data: Optional[Any] = Field(
        default=None, description="Data for the first screen."
    )
