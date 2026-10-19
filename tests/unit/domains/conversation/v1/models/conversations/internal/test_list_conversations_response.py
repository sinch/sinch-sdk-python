from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_response import (
    ListConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)


def test_list_conversations_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListConversationsResponse(
        conversations=[
            {
                "id": "01W4FFL35P4NC4K35CONVERS001",
                "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                "active": True,
                "active_channel": "WHATSAPP",
                "last_received": "2026-10-09T10:00:00Z",
            }
        ],
        next_page_token="token",
        total_size=1,
    )

    assert len(model.conversations) == 1
    conversation = model.conversations[0]
    assert isinstance(conversation, ConversationResponse)
    assert conversation.id == "01W4FFL35P4NC4K35CONVERS001"
    assert conversation.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert conversation.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert conversation.active is True
    assert conversation.active_channel == "WHATSAPP"
    assert conversation.last_received == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
    assert model.next_page_token == "token"
    assert model.total_size == 1
    assert model.content == model.conversations

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "conversations": [
            {
                "id": "01W4FFL35P4NC4K35CONVERS001",
                "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                "active": True,
                "active_channel": "WHATSAPP",
                "last_received": "2026-10-09T10:00:00Z",
            }
        ],
        "next_page_token": "token",
        "total_size": 1,
    }


def test_list_conversations_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListConversationsResponse()

    assert model.conversations is None
    assert model.next_page_token is None
    assert model.total_size is None


def test_list_conversations_response_expects_content_empty_when_conversations_is_none():
    """Test that content returns an empty list when conversations is None."""
    assert ListConversationsResponse().content == []
