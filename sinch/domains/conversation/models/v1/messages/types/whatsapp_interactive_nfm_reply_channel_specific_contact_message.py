from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_interactive_nfm_reply_internal import (
    WhatsAppInteractiveNfmReplyInternal,
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
    nfm_reply: WhatsAppInteractiveNfmReplyInternal = Field(
        ..., description="The nfm reply message."
    )
