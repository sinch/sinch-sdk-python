from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_header_media import (
    WhatsAppInteractiveHeaderMedia,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveVideoHeader(BaseModelConfigurationResponse):
    type: Literal["video"] = Field(
        ..., description="The video associated with the header."
    )
    video: WhatsAppInteractiveHeaderMedia = Field(
        ..., description="The video media object."
    )
