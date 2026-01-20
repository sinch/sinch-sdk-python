import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    FallbackContactMessage,
)


@pytest.fixture
def fallback_contact_message_data():
    return {
        "fallback_message": {
            "raw_message": "raw message value",
            "reason": {
                "code": "RECIPIENT_NOT_OPTED_IN",
                "description": "reason description",
                "sub_code": "UNSPECIFIED_SUB_CODE",
                "channel_code": "a channel code"
            }
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_fallback_contact_message_expects_correct_fields(
    fallback_contact_message_data,
):
    """Test that FallbackContactMessage is parsed correctly with all fields."""
    parsed_response = FallbackContactMessage.model_validate(fallback_contact_message_data)

    assert isinstance(parsed_response, FallbackContactMessage)
    assert parsed_response.fallback_message is not None
    assert parsed_response.fallback_message.raw_message == "raw message value"
    assert parsed_response.fallback_message.reason is not None
    assert parsed_response.fallback_message.reason.code == "RECIPIENT_NOT_OPTED_IN"
    assert parsed_response.fallback_message.reason.description == "reason description"
    assert parsed_response.fallback_message.reason.sub_code == "UNSPECIFIED_SUB_CODE"
    assert parsed_response.fallback_message.reason.channel_code == "a channel code"
    assert parsed_response.reply_to is not None
