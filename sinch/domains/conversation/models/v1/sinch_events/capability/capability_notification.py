from typing import Literal, Optional, Union

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.messages.shared.reason import (
    Reason,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class CapabilityNotification(SinchEvent):
    request_id: Optional[StrictStr] = Field(
        default=None,
        description="ID generated when submitting the capability request. Can be used to detect duplicates.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None, description="The ID of the contact."
    )
    channel: Optional[ConversationChannelType] = None
    identity: Optional[StrictStr] = Field(
        default=None,
        description="The channel identity. For example, a phone number for SMS, WhatsApp, and Viber Business.",
    )
    capability_status: Optional[
        Union[
            Literal[
                "CAPABILITY_UNKNOWN",
                "CAPABILITY_FULL",
                "CAPABILITY_PARTIAL",
                "NO_CAPABILITY",
            ],
            StrictStr,
        ]
    ] = Field(
        default=None,
        description="Status indicating the recipient's capability on the channel.",
    )
    channel_capabilities: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="When capability_status is set to CAPABILITY_PARTIAL, this field includes a list of the supported channel-specific capabilities reported by the channel.",
    )
    reason: Optional[Reason] = None
