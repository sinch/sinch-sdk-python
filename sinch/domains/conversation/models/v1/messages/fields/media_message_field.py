from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.media_properties import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaMessageField(BaseModelConfigurationResponse):
    media_message: Optional[MediaProperties] = None
