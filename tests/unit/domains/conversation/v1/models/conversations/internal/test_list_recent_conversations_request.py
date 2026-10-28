import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_request import (
    ListRecentConversationsRequest,
)


def test_list_recent_conversations_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListRecentConversationsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        only_active=True,
        page_size=5,
        page_token="token_abc",
        order="ASC",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.only_active is True
    assert model.page_size == 5
    assert model.page_token == "token_abc"
    assert model.order == "ASC"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "only_active": True,
        "page_size": 5,
        "page_token": "token_abc",
        "order": "ASC",
    }


def test_list_recent_conversations_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListRecentConversationsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001"
    )

    assert model.only_active is None
    assert model.page_size is None
    assert model.page_token is None
    assert model.order is None


def test_list_recent_conversations_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        ListRecentConversationsRequest(page_size=5)
