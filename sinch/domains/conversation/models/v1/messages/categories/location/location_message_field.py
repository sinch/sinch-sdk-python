from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.location.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class LocationMessageField(BaseModelConfiguration):
    location_message: Optional[LocationMessage] = None
