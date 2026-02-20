from pydantic import Field

from sinch.domains.conversation.models.v1.webhooks.events.conversation_webhook_event_base import (
    ConversationWebhookEventBase,
)
from sinch.domains.conversation.models.v1.webhooks.events.message_submit_notification import (
    MessageSubmitNotification,
)


class MessageSubmitEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_SUBMIT (message submission notification)."""

    message_submit_notification: MessageSubmitNotification = Field(
        description="The message submit notification payload.",
    )
