from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_nfm_reply_name_type import (
    WhatsAppInteractiveNfmReplyNameType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveNfmReplyInternal(BaseModelConfigurationResponse):
    name: WhatsAppInteractiveNfmReplyNameType = Field(
        ..., description="The nfm reply message type."
    )
    response_json: StrictStr = Field(
        ..., description="The JSON specific data."
    )
    body: StrictStr = Field(..., description="The message body.")
