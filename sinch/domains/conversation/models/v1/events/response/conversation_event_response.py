from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.events.shared.app_event import (
    AppEvent,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_direction_type import (
    ConversationDirectionType,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)


class ConversationEventResponse(BaseModelConfiguration):
    app_event: Optional[AppEvent] = Field(
        default=None, description="Event originating from an app"
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="Optional. The ID of the event's conversation. Will not be present for apps in Dispatch Mode.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="Optional. The ID of the contact. Will not be present for apps in Dispatch Mode.",
    )
    channel_identity: ChannelIdentity = Field(default=...)
    accept_time: Optional[datetime] = Field(
        default=None,
        description="The processed time of the message in UTC timezone. Must be less than current_time and greater than (current_time - 30 days).",
    )
    processing_mode: ProcessingModeType = Field(default=...)
    direction: Optional[ConversationDirectionType] = None
    id: StrictStr = Field(default=..., description="The ID of the event.")
