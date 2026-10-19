from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.recent_conversation_response import (
    RecentConversationResponse,
)
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


def test_recent_conversation_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = RecentConversationResponse(
        conversation={
            "id": "01W4FFL35P4NC4K35CONVERS001",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            "active": True,
            "last_received": "2026-10-09T10:00:00Z",
        },
        last_message={
            "id": "01W4FFL35P4NC4K35MESSAGE001",
            "direction": "TO_CONTACT",
            "app_message": {"text_message": {"text": "Hello"}},
            "accept_time": "2026-10-09T10:00:00Z",
        },
    )

    assert isinstance(model.conversation, ConversationResponse)
    assert model.conversation.id == "01W4FFL35P4NC4K35CONVERS001"
    assert model.conversation.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.conversation.active is True
    assert model.conversation.last_received == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
    assert isinstance(model.last_message, AppMessageResponse)
    assert model.last_message.id == "01W4FFL35P4NC4K35MESSAGE001"
    assert model.last_message.direction == "TO_CONTACT"
    assert model.last_message.app_message.text_message.text == "Hello"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "conversation": {
            "id": "01W4FFL35P4NC4K35CONVERS001",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            "active": True,
            "last_received": "2026-10-09T10:00:00Z",
        },
        "last_message": {
            "id": "01W4FFL35P4NC4K35MESSAGE001",
            "direction": "TO_CONTACT",
            "app_message": {"text_message": {"text": "Hello"}},
            "accept_time": "2026-10-09T10:00:00Z",
        },
    }


def test_recent_conversation_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = RecentConversationResponse()

    assert model.conversation is None
    assert model.last_message is None


def test_recent_conversation_response_expects_contact_last_message_resolved():
    """Test that a contact last_message resolves to ContactMessageResponse."""
    model = RecentConversationResponse(
        last_message={
            "id": "01W4FFL35P4NC4K35MESSAGE002",
            "direction": "TO_APP",
            "contact_message": {"text_message": {"text": "Hi"}},
        }
    )

    assert isinstance(model.last_message, ContactMessageResponse)
    assert model.last_message.contact_message.text_message.text == "Hi"
