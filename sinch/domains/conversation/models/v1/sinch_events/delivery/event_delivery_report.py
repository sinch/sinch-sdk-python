from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.messages.shared import (
    ChannelIdentity,
    Reason,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.delivery_status_type import (
    DeliveryStatusType,
)


class EventDeliveryReport(SinchEvent):
    """Delivery report for an app event (EVENT_DELIVERY trigger)."""

    event_id: Optional[StrictStr] = Field(
        default=None, description="The ID of the app event."
    )
    status: Optional[DeliveryStatusType] = Field(
        default=None,
        description="Shows the status of the message or event delivery",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="A unique identity of message recipient on a particular channel. For example, the channel identity on SMS, WHATSAPP or VIBERBM is a MSISDN phone number.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. Will be empty if processing_mode is DISPATCH.",
    )
    reason: Optional[Reason] = Field(default=None)
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata specified when sending the event if any.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Whether or not Conversation API should store contacts and conversations for the app. For more information, see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).",
    )
