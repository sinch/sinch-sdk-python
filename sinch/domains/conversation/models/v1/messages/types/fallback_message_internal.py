from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.reason import Reason
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class FallbackMessageInternal(BaseModelConfigurationResponse):
    raw_message: Optional[StrictStr] = Field(
        default=None,
        description="Optional. The raw fallback message if provided by the channel.",
    )
    reason: Optional[Reason] = None
