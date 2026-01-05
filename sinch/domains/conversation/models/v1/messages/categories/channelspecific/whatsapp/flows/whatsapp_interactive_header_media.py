from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveHeaderMedia(BaseModelConfigurationResponse):
    link: StrictStr = Field(..., description="URL for the media.")
