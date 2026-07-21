from typing import Optional
from pydantic import Field, StrictBool
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class SmartConversation(BaseModelConfiguration):
    enabled: Optional[StrictBool] = Field(
        default=None,
        description="Set to true to allow messages processed by this app to be analyzed by Smart Conversations.",
    )
