from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_header_media import (
    WhatsAppInteractiveHeaderMedia,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveImageHeader(BaseModelConfigurationResponse):
    type: Literal["image"] = Field(
        ..., description="The image associated with the header."
    )
    image: WhatsAppInteractiveHeaderMedia = Field(
        ..., description="The image media object."
    )
