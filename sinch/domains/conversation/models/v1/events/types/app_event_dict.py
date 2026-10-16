from typing import Any, Dict, TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.events.types.agent_dict import (
    AgentDict,
)


class CommentReplyEventDict(TypedDict):
    text: str


class AgentEventDict(TypedDict):
    agent: AgentDict


class GenericEventDict(TypedDict):
    payload: Dict[str, Any]


class AppEventDict(TypedDict):
    composing_event: NotRequired[Dict[str, Any]]
    composing_end_event: NotRequired[Dict[str, Any]]
    read_message_event: NotRequired[Dict[str, Any]]
    comment_reply_event: NotRequired[CommentReplyEventDict]
    agent_joined_event: NotRequired[AgentEventDict]
    agent_left_event: NotRequired[AgentEventDict]
    generic_event: NotRequired[GenericEventDict]
