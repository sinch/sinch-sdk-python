from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.conversations.internal.inject_event_request import (
    InjectEventRequest,
)
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    ComposingAppEvent,
    GenericAppEvent,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)

ACCEPT_TIME = datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


def test_inject_event_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InjectEventRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        app_event={"generic_event": {"payload": {"key": "value"}}},
        accept_time=ACCEPT_TIME,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identity={"channel": "RCS", "identity": "+46701234567"},
        processing_mode="CONVERSATION",
    )

    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert isinstance(model.app_event, GenericAppEvent)
    assert model.app_event.generic_event.payload == {"key": "value"}
    assert model.accept_time == ACCEPT_TIME
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "RCS"
    assert model.channel_identity.identity == "+46701234567"
    assert model.processing_mode == "CONVERSATION"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
        "app_event": {"generic_event": {"payload": {"key": "value"}}},
        "accept_time": "2026-10-09T10:00:00Z",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "channel_identity": {"channel": "RCS", "identity": "+46701234567"},
        "processing_mode": "CONVERSATION",
    }


def test_inject_event_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = InjectEventRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        accept_time=ACCEPT_TIME,
    )

    assert model.app_event is None
    assert model.contact_id is None
    assert model.channel_identity is None
    assert model.processing_mode is None


def test_inject_event_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        InjectEventRequest(conversation_id="01W4FFL35P4NC4K35CONVERS001")


def test_inject_event_request_expects_composing_event_variant_accepted():
    """Test that the composing event variant of app_event is accepted."""
    model = InjectEventRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        app_event={"composing_event": {}},
        accept_time=ACCEPT_TIME,
    )

    assert isinstance(model.app_event, ComposingAppEvent)
