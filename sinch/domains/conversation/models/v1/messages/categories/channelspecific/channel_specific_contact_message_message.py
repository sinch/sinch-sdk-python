from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.nfmreply.whatsapp_interactive_nfm_reply_message import (
    WhatsAppInteractiveNfmReplyMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificContactMessageMessage(BaseModelConfigurationResponse):
    message_type: Literal["nfm_reply"] = Field(
        ..., description="The message type."
    )
    message: WhatsAppInteractiveNfmReplyMessage = Field(
        ..., description="The message content."
    )
