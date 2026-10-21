from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.message.inbound_message import (
    InboundMessage,
)


class MessageInboundSmartConversationRedactionEvent(
    ConversationSinchEventBase
):
    """Sinch Event for MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION (inbound message after Smart Conversations redaction)."""

    message_redaction: InboundMessage = Field(
        description="The inbound message payload, redacted if required.",
    )
