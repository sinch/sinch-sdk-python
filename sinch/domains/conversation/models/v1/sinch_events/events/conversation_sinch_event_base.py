from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ConversationSinchEventBase(SinchEvent):
    """Base fields present on every Conversation API Sinch Event payload."""

    app_id: StrictStr = Field(
        description="Id of the subscribed app.",
    )
    project_id: StrictStr = Field(
        description="The project ID of the app which has subscribed for the callback.",
    )
    accepted_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the channel callback was accepted by the Conversation API.",
    )
    event_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the event as provided by the underlying channels.",
    )
    message_metadata: Optional[StrictStr] = Field(
        default=None,
        description="Context-dependent metadata.",
    )
    correlation_id: Optional[StrictStr] = Field(
        default=None,
        description="Value from correlation_id of the send message request.",
    )
