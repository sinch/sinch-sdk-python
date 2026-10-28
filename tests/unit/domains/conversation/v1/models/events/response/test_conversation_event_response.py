from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)


def test_conversation_event_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationEventResponse(
        id="01W4FFL35P4NC4K35EVENT0001",
        direction="TO_CONTACT",
        app_event={"composing_event": {}},
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identity={"channel": "SMS", "identity": "46700000000"},
        accept_time="2026-10-09T10:00:00Z",
        processing_mode="CONVERSATION",
    )

    assert model.id == "01W4FFL35P4NC4K35EVENT0001"
    assert model.direction == "TO_CONTACT"
    assert model.app_event.composing_event == {}
    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "SMS"
    assert model.channel_identity.identity == "46700000000"
    assert model.accept_time == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
    assert model.processing_mode == "CONVERSATION"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["id"] == "01W4FFL35P4NC4K35EVENT0001"
    assert alias_dump["direction"] == "TO_CONTACT"
    assert alias_dump["app_event"] == {"composing_event": {}}
    assert alias_dump["conversation_id"] == "01W4FFL35P4NC4K35CONVERS001"
    assert alias_dump["contact_id"] == "01W4FFL35P4NC4K35CONTACT001"
    assert alias_dump["channel_identity"] == {
        "channel": "SMS",
        "identity": "46700000000",
    }
    assert alias_dump["accept_time"] == "2026-10-09T10:00:00Z"
    assert alias_dump["processing_mode"] == "CONVERSATION"


def test_conversation_event_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ConversationEventResponse(
        id="01W4FFL35P4NC4K35EVENT0001",
        channel_identity={"channel": "SMS", "identity": "46700000000"},
        processing_mode="DISPATCH",
    )

    assert model.app_event is None
    assert model.conversation_id is None
    assert model.contact_id is None
    assert model.accept_time is None
    assert model.direction is None


@pytest.mark.parametrize(
    "missing", ["id", "channel_identity", "processing_mode"]
)
def test_conversation_event_response_expects_validation_error_for_missing_required(
    missing,
):
    """Test that id, channel_identity and processing_mode are required."""
    data = {
        "id": "01W4FFL35P4NC4K35EVENT0001",
        "channel_identity": {"channel": "SMS", "identity": "46700000000"},
        "processing_mode": "CONVERSATION",
    }
    del data[missing]

    with pytest.raises(ValidationError):
        ConversationEventResponse(**data)
