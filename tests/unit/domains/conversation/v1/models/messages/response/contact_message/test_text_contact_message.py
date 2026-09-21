import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    TextContactMessage,
)


@pytest.fixture
def text_contact_message_data():
    return {
        "text_message": {
            "text": "This is a text message."
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_text_contact_message_expects_correct_fields(text_contact_message_data):
    """Test that TextContactMessage is parsed correctly with reply_to present."""
    parsed_response = TextContactMessage.model_validate(text_contact_message_data)

    assert isinstance(parsed_response, TextContactMessage)
    assert parsed_response.text_message is not None
    assert parsed_response.text_message.text == "This is a text message."
    assert parsed_response.reply_to is not None


def test_parsing_text_contact_message_allows_missing_reply_to():
    """Test that TextContactMessage accepts payloads without reply_to."""
    parsed_response = TextContactMessage.model_validate(
        {
            "text_message": {
                "text": "This is a text message."
            }
        }
    )

    assert isinstance(parsed_response, TextContactMessage)
    assert parsed_response.text_message is not None
    assert parsed_response.text_message.text == "This is a text message."
    assert parsed_response.reply_to is None


def test_parsing_text_contact_message_allows_null_reply_to():
    """Test that TextContactMessage accepts payloads with reply_to set to null."""
    parsed_response = TextContactMessage.model_validate(
        {
            "text_message": {
                "text": "This is a text message."
            },
            "reply_to": None
        }
    )

    assert isinstance(parsed_response, TextContactMessage)
    assert parsed_response.text_message is not None
    assert parsed_response.text_message.text == "This is a text message."
    assert parsed_response.reply_to is None
