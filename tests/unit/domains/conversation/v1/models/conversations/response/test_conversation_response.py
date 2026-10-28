from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)


def test_conversation_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationResponse(
        id="01W4FFL35P4NC4K35CONVERS001",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        active=True,
        active_channel="WHATSAPP",
        metadata="legacy metadata",
        metadata_json={"key": "value"},
        correlation_id="correlation-1",
        last_received="2026-10-09T10:00:00Z",
    )

    assert model.id == "01W4FFL35P4NC4K35CONVERS001"
    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.active is True
    assert model.active_channel == "WHATSAPP"
    assert model.metadata == "legacy metadata"
    assert model.metadata_json == {"key": "value"}
    assert model.correlation_id == "correlation-1"
    assert model.last_received == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "id": "01W4FFL35P4NC4K35CONVERS001",
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "active": True,
        "active_channel": "WHATSAPP",
        "metadata": "legacy metadata",
        "metadata_json": {"key": "value"},
        "correlation_id": "correlation-1",
        "last_received": "2026-10-09T10:00:00Z",
    }


def test_conversation_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ConversationResponse()

    assert model.id is None
    assert model.app_id is None
    assert model.contact_id is None
    assert model.active is None
    assert model.active_channel is None
    assert model.metadata is None
    assert model.metadata_json is None
    assert model.correlation_id is None
    assert model.last_received is None
