from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_nfm_reply import (
    WhatsAppInteractiveNfmReply,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveNfmReplyChannelSpecificContactMessage(
    BaseModelConfigurationResponse
):
    type: Literal["nfm_reply"] = Field(
        description="The interactive message type."
    )
    nfm_reply: WhatsAppInteractiveNfmReply = Field(
        ..., description="The nfm reply message."
    )
