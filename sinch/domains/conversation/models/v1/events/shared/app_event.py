from typing import Annotated, Any, Dict, Union

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.events.shared.agent_joined_event import (
    AgentJoinedEvent,
)
from sinch.domains.conversation.models.v1.events.shared.agent_left_event import (
    AgentLeftEvent,
)
from sinch.domains.conversation.models.v1.events.shared.comment_reply_event import (
    CommentReplyEvent,
)
from sinch.domains.conversation.models.v1.events.shared.generic_event import (
    GenericEvent,
)


class ComposingAppEvent(BaseModelConfiguration):
    composing_event: Dict[str, Any]


class ComposingEndAppEvent(BaseModelConfiguration):
    composing_end_event: Dict[str, Any]


class ReadMessageAppEvent(BaseModelConfiguration):
    read_message_event: Dict[str, Any]


class CommentReplyAppEvent(BaseModelConfiguration):
    comment_reply_event: CommentReplyEvent


class AgentJoinedAppEvent(BaseModelConfiguration):
    agent_joined_event: AgentJoinedEvent


class AgentLeftAppEvent(BaseModelConfiguration):
    agent_left_event: AgentLeftEvent


class GenericAppEvent(BaseModelConfiguration):
    generic_event: GenericEvent


AppEvent = Annotated[
    Union[
        ComposingAppEvent,
        ComposingEndAppEvent,
        ReadMessageAppEvent,
        CommentReplyAppEvent,
        AgentJoinedAppEvent,
        AgentLeftAppEvent,
        GenericAppEvent,
    ],
    ResolveUnion(),
]
