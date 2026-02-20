from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.webhooks.v1.internal import WebhookEvent
from sinch.domains.conversation.models.v1.messages.shared import (
    ChannelIdentity,
    Reason,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)

from sinch.domains.conversation.models.v1.webhooks.events.message_delivery_status_type import (
    MessageDeliveryStatusType,
)


class MessageDeliveryReport(WebhookEvent):
    """Delivery report for an app message (MESSAGE_DELIVERY trigger)."""

    message_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the message.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation.",
    )
    status: Optional[MessageDeliveryStatusType] = Field(
        default=None,
        description="Shows the status of the message or event delivery.",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="Channel identity of the recipient.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact.",
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata associated with the message.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Processing mode (CONVERSATION or DISPATCH).",
    )
    reason: Optional[Reason] = Field(
        default=None,
        description="Reason when status is FAILED.",
    )
