from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows import (
    WhatsAppInteractiveHeaderMedia,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class WhatsAppInteractiveVideoHeader(BaseModelConfiguration):
    type: Literal["video"] = Field(
        ..., description="The video associated with the header."
    )
    video: WhatsAppInteractiveHeaderMedia = Field(
        ..., description="The video media object."
    )
