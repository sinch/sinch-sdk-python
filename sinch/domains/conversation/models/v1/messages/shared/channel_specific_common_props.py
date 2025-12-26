from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_header_internal import (
    WhatsAppInteractiveHeaderInternal,
)
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_body import (
    WhatsAppInteractiveBody,
)
from sinch.domains.conversation.models.v1.messages.types.whatsapp_interactive_footer import (
    WhatsAppInteractiveFooter,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificCommonProps(BaseModelConfigurationResponse):
    header: Optional[WhatsAppInteractiveHeaderInternal] = Field(
        default=None, description="The header of the interactive message."
    )
    body: Optional[WhatsAppInteractiveBody] = Field(
        default=None, description="Body of the interactive message."
    )
    footer: Optional[WhatsAppInteractiveFooter] = Field(
        default=None, description="Footer of the interactive message."
    )
