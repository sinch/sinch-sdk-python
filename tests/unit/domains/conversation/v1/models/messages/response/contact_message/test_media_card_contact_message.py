import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    MediaCardContactMessage,
)


@pytest.fixture
def media_card_contact_message_data():
    return {
        "media_card_message": {
            "caption": "caption value",
            "url": "an url value"
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_media_card_contact_message_expects_correct_fields(
    media_card_contact_message_data,
):
    """Test that MediaCardContactMessage is parsed correctly with all fields."""
    parsed_response = MediaCardContactMessage.model_validate(
        media_card_contact_message_data
    )

    assert isinstance(parsed_response, MediaCardContactMessage)
    assert parsed_response.media_card_message is not None
    assert parsed_response.media_card_message.caption == "caption value"
    assert parsed_response.media_card_message.url == "an url value"
    assert parsed_response.reply_to is not None
