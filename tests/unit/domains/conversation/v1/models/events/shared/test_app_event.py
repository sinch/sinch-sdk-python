import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    AgentJoinedAppEvent,
    AgentLeftAppEvent,
    AppEvent,
    CommentReplyAppEvent,
    ComposingAppEvent,
    ComposingEndAppEvent,
    GenericAppEvent,
    ReadMessageAppEvent,
)

adapter = TypeAdapter(AppEvent)

AGENT = {
    "display_name": "Agent Smith",
    "type": "HUMAN",
    "picture_url": "https://example.com/agent.png",
}


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"composing_event": {}}, ComposingAppEvent),
        ({"composing_end_event": {}}, ComposingEndAppEvent),
        ({"read_message_event": {}}, ReadMessageAppEvent),
        ({"comment_reply_event": {"text": "thanks"}}, CommentReplyAppEvent),
        ({"agent_joined_event": {"agent": AGENT}}, AgentJoinedAppEvent),
        ({"agent_left_event": {"agent": AGENT}}, AgentLeftAppEvent),
        ({"generic_event": {"payload": {"a": 1}}}, GenericAppEvent),
    ],
    ids=[
        "composing",
        "composing_end",
        "read_message",
        "comment_reply",
        "agent_joined",
        "agent_left",
        "generic",
    ],
)
def test_app_event_expects_each_variant_resolved(payload, expected_model):
    """Test that each oneOf variant is resolved from the event key it declares."""
    assert type(adapter.validate_python(payload)) is expected_model


@pytest.mark.parametrize(
    "payload",
    [{"unknown_event": {}}, {}],
    ids=["unknown_event_key", "no_event_key"],
)
def test_app_event_expects_validation_error_on_unknown_event(payload):
    """Test that an event the SDK does not know is rejected when a request is
    being built."""
    with pytest.raises(ValidationError):
        adapter.validate_python(payload)


def test_app_event_expects_unknown_event_parsed_in_a_response():
    """Test that an event added to the API later is parsed as SinchRawResponse
    instead of failing the whole response."""
    payload = {"unknown_event": {"a": 1}}

    with response_parsing_scope():
        event = adapter.validate_python(payload)

    assert isinstance(event, SinchRawResponse)
    assert event.model_dump() == payload
