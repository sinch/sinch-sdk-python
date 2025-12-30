from typing import Literal, Union, Annotated
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_nfm_reply_channel_specific_contact_message import (
    WhatsAppInteractiveNfmReplyChannelSpecificContactMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificContactMessageMessage(BaseModelConfigurationResponse):
    message_type: Literal["nfm_reply"] = Field(
        ..., description="The message type."
    )
    message: Annotated[
        Union[WhatsAppInteractiveNfmReplyChannelSpecificContactMessage],
        Field(discriminator="type"),
    ] = Field(..., description="The message content.")
