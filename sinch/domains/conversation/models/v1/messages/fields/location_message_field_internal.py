from typing import Optional
from sinch.domains.conversation.models.v1.messages.types.location_message_internal import (
    LocationMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class LocationMessageFieldInternal(BaseModelConfigurationResponse):
    location_message: Optional[LocationMessageInternal] = None
