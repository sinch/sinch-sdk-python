from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_response import (
    ListRecentConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.recent_conversation_response import (
    RecentConversationResponse,
)


def test_list_recent_conversations_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListRecentConversationsResponse(
        conversations=[
            {
                "conversation": {"id": "01W4FFL35P4NC4K35CONVERS001"},
                "last_message": {
                    "id": "01W4FFL35P4NC4K35MESSAGE001",
                    "app_message": {"text_message": {"text": "Hello"}},
                },
            }
        ],
        next_page_token="token",
        total_size=1,
    )

    assert len(model.conversations) == 1
    recent = model.conversations[0]
    assert isinstance(recent, RecentConversationResponse)
    assert recent.conversation.id == "01W4FFL35P4NC4K35CONVERS001"
    assert recent.last_message.id == "01W4FFL35P4NC4K35MESSAGE001"
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
                "conversation": {"id": "01W4FFL35P4NC4K35CONVERS001"},
                "last_message": {
                    "id": "01W4FFL35P4NC4K35MESSAGE001",
                    "app_message": {"text_message": {"text": "Hello"}},
                },
            }
        ],
        "next_page_token": "token",
        "total_size": 1,
    }


def test_list_recent_conversations_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListRecentConversationsResponse()

    assert model.conversations is None
    assert model.next_page_token is None
    assert model.total_size is None


def test_list_recent_conversations_response_expects_content_empty_when_conversations_is_none():
    """Test that content returns an empty list when conversations is None."""
    assert ListRecentConversationsResponse().content == []
