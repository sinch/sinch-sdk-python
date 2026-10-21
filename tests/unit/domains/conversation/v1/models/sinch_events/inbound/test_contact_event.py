import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    ComposingAppEvent,
    ComposingEndAppEvent,
    GenericAppEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.contact_event import (
    CommentContactEvent,
    ContactEvent,
    ConversationDeletedContactEvent,
)

adapter = TypeAdapter(ContactEvent)


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"composing_event": {}}, ComposingAppEvent),
        ({"composing_end_event": {}}, ComposingEndAppEvent),
        ({"conversation_deleted_event": {}}, ConversationDeletedContactEvent),
        ({"comment_event": {"text": "Nice!"}}, CommentContactEvent),
        ({"generic_event": {"payload": {"a": 1}}}, GenericAppEvent),
    ],
    ids=[
        "composing",
        "composing_end",
        "conversation_deleted",
        "comment",
        "generic",
    ],
)
def test_contact_event_expects_each_variant_resolved(payload, expected_model):
    """Test that each oneOf variant is resolved from the event key it declares."""
    assert type(adapter.validate_python(payload)) is expected_model



@pytest.mark.parametrize(
    "payload",
    [{"unknown_event": {}}, {}, {"comment_event": {}}],
    ids=["unknown_event_key", "no_event_key", "comment_without_text"],
)
def test_contact_event_expects_validation_error_on_invalid_payload(payload):
    """Test that an unknown event or a known one with invalid content is rejected outside a response."""
    with pytest.raises(ValidationError):
        adapter.validate_python(payload)


def test_contact_event_expects_unknown_event_parsed_in_a_response():
    """Test that an event added to the API later is parsed as SinchRawResponse
    instead of failing the whole event."""
    payload = {"unknown_event": {"a": 1}}

    with response_parsing_scope():
        event = adapter.validate_python(payload)

    assert isinstance(event, SinchRawResponse)
    assert event.model_dump() == payload
