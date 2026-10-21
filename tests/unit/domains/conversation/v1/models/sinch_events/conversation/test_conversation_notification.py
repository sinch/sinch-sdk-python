from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_notification import (
    ConversationNotification,
)


def test_conversation_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationNotification(
        conversation={
            "id": "01W4FFL35P4NC4K35CONVERS01",
            "app_id": "01W4FFL35P4NC4K35CONVAPP01",
            "contact_id": "01W4FFL35P4NC4K35CONTACT01",
            "active": True,
            "active_channel": "WHATSAPP",
        }
    )

    assert isinstance(model.conversation, ConversationResponse)
    assert model.conversation.id == "01W4FFL35P4NC4K35CONVERS01"
    assert model.conversation.app_id == "01W4FFL35P4NC4K35CONVAPP01"
    assert model.conversation.contact_id == "01W4FFL35P4NC4K35CONTACT01"
    assert model.conversation.active is True
    assert model.conversation.active_channel == "WHATSAPP"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["conversation"] == {
        "id": "01W4FFL35P4NC4K35CONVERS01",
        "app_id": "01W4FFL35P4NC4K35CONVAPP01",
        "contact_id": "01W4FFL35P4NC4K35CONTACT01",
        "active": True,
        "active_channel": "WHATSAPP",
    }


def test_conversation_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ConversationNotification()

    assert model.conversation is None
