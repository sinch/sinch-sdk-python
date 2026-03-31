from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class WhatsAppInteractiveHeaderMedia(BaseModelConfiguration):
    link: StrictStr = Field(..., description="URL for the media.")
