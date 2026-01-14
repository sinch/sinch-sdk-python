from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows import (
    WhatsAppInteractiveHeaderMedia,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveDocumentHeader(BaseModelConfigurationResponse):
    type: Literal["document"] = Field(
        ..., description="The document associated with the header."
    )
    document: WhatsAppInteractiveHeaderMedia = Field(
        ..., description="The document media object."
    )
