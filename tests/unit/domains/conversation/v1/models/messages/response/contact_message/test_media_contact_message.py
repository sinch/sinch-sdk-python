import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    MediaContactMessage,
)


@pytest.fixture
def media_contact_message_data():
    return {
        "media_message": {
            "thumbnail_url": "another url",
            "url": "an url value",
            "filename_override": "filename override value"
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_media_contact_message_expects_correct_fields(media_contact_message_data):
    """Test that MediaContactMessage is parsed correctly with all fields."""
    parsed_response = MediaContactMessage.model_validate(media_contact_message_data)

    assert isinstance(parsed_response, MediaContactMessage)
    assert parsed_response.media_message is not None
    assert parsed_response.media_message.thumbnail_url == "another url"
    assert parsed_response.media_message.url == "an url value"
    assert parsed_response.media_message.filename_override == "filename override value"
    assert parsed_response.reply_to is not None
