from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_delivery_report import (
    MessageDeliveryReport,
)


class MessageDeliveryReceiptEvent(ConversationSinchEventBase):
    """Sinch Event for MESSAGE_DELIVERY (delivery receipt for app messages)."""

    message_delivery_report: MessageDeliveryReport = Field(
        default=None,
        description="The delivery report payload.",
    )
