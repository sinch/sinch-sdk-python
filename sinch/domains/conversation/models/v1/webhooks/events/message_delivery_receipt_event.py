from pydantic import Field

from sinch.domains.conversation.models.v1.webhooks.events.conversation_webhook_event_base import (
    ConversationWebhookEventBase,
)
from sinch.domains.conversation.models.v1.webhooks.events.message_delivery_report import (
    MessageDeliveryReport,
)


class MessageDeliveryReceiptEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_DELIVERY (delivery receipt for app messages)."""

    message_delivery_report: MessageDeliveryReport = Field(
        default=None,
        description="The delivery report payload.",
    )
