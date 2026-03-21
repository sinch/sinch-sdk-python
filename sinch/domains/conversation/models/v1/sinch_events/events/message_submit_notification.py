from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.messages.shared import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.messages.response.types.app_message import (
    AppMessage,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)


class MessageSubmitNotification(SinchEvent):
    """Notification that an app message was submitted (MESSAGE_SUBMIT trigger)."""

    message_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the app message.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation. Empty if processing_mode is DISPATCH.",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="Channel identity of the recipient.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. Empty if processing_mode is DISPATCH.",
    )
    submitted_message: Optional[AppMessage] = Field(
        default=None,
        description="The submitted app message content (AppMessage).",
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata from message_metadata of the Send Message request.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Processing mode (CONVERSATION or DISPATCH).",
    )
