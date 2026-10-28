import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.sinch_events.inbound.contact_message_event import (
    ContactMessageEvent,
    PaymentStatusUpdateContactMessageEvent,
    ReactionContactMessageEvent,
    ShortLinkActivatedContactMessageEvent,
)

adapter = TypeAdapter(ContactMessageEvent)

REACTION = {
    "emoji": "thumbs_up",
    "action": "REACTION_ACTION_REACT",
    "message_id": "message-1",
}


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        (
            {"payment_status_update_event": {"reference_id": "order-1"}},
            PaymentStatusUpdateContactMessageEvent,
        ),
        (
            {"shortlink_activated_event": {"ref": "campaign"}},
            ShortLinkActivatedContactMessageEvent,
        ),
        ({"reaction_event": REACTION}, ReactionContactMessageEvent),
    ],
    ids=["payment_status_update", "shortlink_activated", "reaction"],
)
def test_contact_message_event_expects_each_variant_resolved(payload, expected_model):
    """Test that each oneOf variant is resolved from the event key it declares."""
    assert type(adapter.validate_python(payload)) is expected_model


def test_contact_message_event_expects_reaction_content_parsed():
    """Test that the reaction variant keeps the content of the reaction."""
    event = adapter.validate_python({"reaction_event": REACTION})

    assert event.reaction_event.emoji == "thumbs_up"
    assert event.reaction_event.action == "REACTION_ACTION_REACT"
    assert event.reaction_event.message_id == "message-1"


@pytest.mark.parametrize(
    "payload",
    [{"unknown_event": {}}, {}, {"reaction_event": {"emoji": "thumbs_up"}}],
    ids=["unknown_event_key", "no_event_key", "reaction_missing_required_fields"],
)
def test_contact_message_event_expects_validation_error_on_invalid_payload(payload):
    """Test that an unknown event or a known one with invalid content is rejected outside a response."""
    with pytest.raises(ValidationError):
        adapter.validate_python(payload)


def test_contact_message_event_expects_unknown_event_parsed_in_a_response():
    """Test that an event added to the API later is parsed as SinchRawResponse
    instead of failing the whole event."""
    payload = {"unknown_event": {"a": 1}}

    with response_parsing_scope():
        event = adapter.validate_python(payload)

    assert isinstance(event, SinchRawResponse)
    assert event.model_dump() == payload
