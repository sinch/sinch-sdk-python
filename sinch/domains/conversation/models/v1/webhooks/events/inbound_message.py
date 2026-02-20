from typing import Optional

from pydantic import Field

from sinch.domains.conversation.webhooks.v1.internal import WebhookEvent
from sinch.domains.conversation.models.v1.messages.shared.message_common_props import (
    MessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (
    ContactMessage,
)


class InboundMessage(MessageCommonProps, WebhookEvent):
    """Inbound message container (contact message + channel/contact info)."""

    contact_message: Optional[ContactMessage] = Field(
        default=None,
        description="The contact (inbound) message content.",
    )
