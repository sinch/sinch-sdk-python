import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.conversations.internal.update_conversation_request import (
    UpdateConversationRequest,
)


def test_update_conversation_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UpdateConversationRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        metadata_update_strategy="MERGE_PATCH",
        active=True,
        active_channel="WHATSAPP",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        metadata="legacy metadata",
        metadata_json={"key": "value"},
        correlation_id="correlation-1",
    )

    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert model.metadata_update_strategy == "MERGE_PATCH"
    assert model.active is True
    assert model.active_channel == "WHATSAPP"
    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.metadata == "legacy metadata"
    assert model.metadata_json == {"key": "value"}
    assert model.correlation_id == "correlation-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
        "metadata_update_strategy": "MERGE_PATCH",
        "active": True,
        "active_channel": "WHATSAPP",
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "metadata": "legacy metadata",
        "metadata_json": {"key": "value"},
        "correlation_id": "correlation-1",
    }


def test_update_conversation_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = UpdateConversationRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001"
    )

    assert model.metadata_update_strategy is None
    assert model.active is None
    assert model.active_channel is None
    assert model.app_id is None
    assert model.contact_id is None
    assert model.metadata is None
    assert model.metadata_json is None
    assert model.correlation_id is None


def test_update_conversation_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        UpdateConversationRequest(active=True)
