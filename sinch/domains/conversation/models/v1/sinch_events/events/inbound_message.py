from typing import Optional

from pydantic import Field

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.messages.shared.message_common_props import (
    MessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (
    ContactMessage,
)


class InboundMessage(MessageCommonProps, SinchEvent):
    """Inbound message container (contact message + channel/contact info)."""

    contact_message: Optional[ContactMessage] = Field(
        default=None,
        description="The contact (inbound) message content.",
    )
