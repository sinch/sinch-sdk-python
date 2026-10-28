import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.conversations.internal.conversation_id_request import (
    ConversationIdRequest,
)


def test_conversation_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationIdRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001"
    )

    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["conversation_id"] == "01W4FFL35P4NC4K35CONVERS001"


def test_conversation_id_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        ConversationIdRequest()
