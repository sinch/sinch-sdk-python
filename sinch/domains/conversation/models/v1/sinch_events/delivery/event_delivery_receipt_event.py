from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.event_delivery_report import (
    EventDeliveryReport,
)


class EventDeliveryReceiptEvent(ConversationSinchEventBase):
    """Sinch Event for EVENT_DELIVERY (delivery receipt for app events)."""

    event_delivery_report: EventDeliveryReport = Field(
        description="The event delivery report payload.",
    )
