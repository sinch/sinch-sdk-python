from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.media.media_properties import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class MediaMessageField(BaseModelConfiguration):
    media_message: Optional[MediaProperties] = None
