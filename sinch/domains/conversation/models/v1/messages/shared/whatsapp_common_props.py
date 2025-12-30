from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.types.whatsapp_interactive_header import (
    WhatsAppInteractiveHeader,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_body import (
    WhatsAppInteractiveBody,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_footer import (
    WhatsAppInteractiveFooter,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppCommonProps(BaseModelConfigurationResponse):
    header: Optional[WhatsAppInteractiveHeader] = Field(
        default=None, description="The header of the interactive message."
    )
    body: Optional[WhatsAppInteractiveBody] = Field(
        default=None, description="Body of the interactive message."
    )
    footer: Optional[WhatsAppInteractiveFooter] = Field(
        default=None, description="Footer of the interactive message."
    )
