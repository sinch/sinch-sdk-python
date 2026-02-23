from pydantic import Field

from sinch.domains.conversation.models.v1.webhooks.events.conversation_webhook_event_base import (
    ConversationWebhookEventBase,
)
from sinch.domains.conversation.models.v1.webhooks.events.inbound_message import (
    InboundMessage,
)


class MessageInboundEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_INBOUND (inbound message from user)."""

    message: InboundMessage = Field(
        description="The inbound message payload.",
    )
