from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.inbound.reaction_action_type import (
    ReactionActionType,
)


class ReactionEvent(SinchEvent):
    emoji: StrictStr = Field(
        default=...,
        description='Indicates that an emoji reaction was placed on a message. This value is the string representation of the emoji. For example: "&#2764&#FE0F"',
    )
    action: ReactionActionType = Field(
        default=..., description="Type of action"
    )
    message_id: StrictStr = Field(
        default=...,
        description="The ID of the MT message that this reaction is associated with.",
    )
    reaction_category: Optional[StrictStr] = Field(
        default=None,
        description='If present, represents the grouping of emojis. Example values: "smile", "angry", "sad", "wow", "love", "like", "dislike", "other"',
    )
