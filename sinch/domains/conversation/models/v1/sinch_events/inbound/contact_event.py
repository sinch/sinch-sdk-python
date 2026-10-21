from typing import Annotated, Any, Dict, Union

from pydantic import Field

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    ComposingAppEvent,
    ComposingEndAppEvent,
    GenericAppEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.comment_event import (
    CommentEvent,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ConversationDeletedContactEvent(SinchEvent):
    conversation_deleted_event: Dict[str, Any] = Field(
        description="An empty object. Represents a conversation deleted by the contact.",
    )


class CommentContactEvent(SinchEvent):
    comment_event: CommentEvent = Field(
        description="Object which contains information of a comment made by an user outside of the main conversation context. Currently only supported on Instagram channel, see Instagram Private Replies for more details",
    )


ContactEvent = Annotated[
    Union[
        ComposingAppEvent,
        ComposingEndAppEvent,
        ConversationDeletedContactEvent,
        CommentContactEvent,
        GenericAppEvent,
    ],
    ResolveUnion(),
]
