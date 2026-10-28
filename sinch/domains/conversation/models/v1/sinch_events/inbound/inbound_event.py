from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.messages.types.conversation_direction_type import (
    ConversationDirectionType,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.contact_event import (
    ContactEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.contact_message_event import (
    ContactMessageEvent,
)


class InboundEvent(SinchEvent):
    """Inbound event container (contact event + channel/contact info)."""

    id: Optional[StrictStr] = Field(default=None, description="The event ID.")
    direction: Optional[ConversationDirectionType] = Field(
        default=None,
        description="The direction of the event. It's always TO_APP for contact events.",
    )
    contact_event: Optional[ContactEvent] = Field(
        default=None, description="Message originating from a contact"
    )
    contact_message_event: Optional[ContactMessageEvent] = Field(
        default=None,
        description="The content of the event when contact_event is not populated. Note that this object is currently only available to select customers for beta testing. Mutually exclusive with contact_event.",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="A unique identity of message recipient on a particular channel. For example, the channel identity on SMS, WHATSAPP or VIBERBM is a MSISDN phone number.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. Will be empty if processing_mode is DISPATCH.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation this event is part of. Will be empty if processing_mode is DISPATCH.",
    )
    accept_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp marking when the channel callback was received by the Conversation API.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Whether or not Conversation API should store contacts and conversations for the app. For more information, see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).",
    )
