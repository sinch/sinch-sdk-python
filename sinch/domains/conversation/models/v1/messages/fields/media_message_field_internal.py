from typing import Optional
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaMessageFieldInternal(BaseModelConfigurationResponse):
    media_message: Optional[MediaPropertiesInternal] = None
