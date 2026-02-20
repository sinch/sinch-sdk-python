from typing import Union

from sinch.domains.conversation.models.v1.webhooks.events.conversation_webhook_event_base import (
    ConversationWebhookEventBase,
)
from sinch.domains.conversation.models.v1.webhooks.events.message_delivery_receipt_event import (
    MessageDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.webhooks.events.message_inbound_event import (
    MessageInboundEvent,
)
from sinch.domains.conversation.models.v1.webhooks.events.message_submit_event import (
    MessageSubmitEvent,
)


ConversationWebhookEvent = Union[
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
    ConversationWebhookEventBase,
]
