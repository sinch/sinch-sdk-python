from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class LocationMessageField(BaseModelConfigurationResponse):
    location_message: Optional[LocationMessage] = None
