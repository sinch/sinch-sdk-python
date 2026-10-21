from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.messages.shared.reason import (
    Reason,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class RecordNotification(SinchEvent):
    entity_id: Optional[StrictStr] = Field(
        default=None, description="The ID of the entity."
    )
    record_status: Optional[
        Union[
            Literal["RECORD_STATUS_UNSPECIFIED", "EVENT_RECORD_STORED"],
            StrictStr,
        ]
    ] = Field(default=None, description="Record status for a specific entity")
    channel_identity: Optional[ChannelIdentity] = None
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. Will not be present for apps in Dispatch Mode.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation. Will not be present for apps in Dispatch Mode.",
    )
    reason: Optional[Reason] = None
    processing_mode: Optional[ProcessingModeType] = None
