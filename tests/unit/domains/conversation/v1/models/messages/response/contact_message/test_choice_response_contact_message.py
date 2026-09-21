import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    ChoiceResponseContactMessage,
)


@pytest.fixture
def choice_response_contact_message_data():
    return {
        "choice_response_message": {
            "message_id": "message id value",
            "postback_data": "postback data value"
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_choice_response_contact_message_expects_correct_fields(
    choice_response_contact_message_data,
):
    """Test that ChoiceResponseContactMessage is parsed correctly with all fields."""
    parsed_response = ChoiceResponseContactMessage.model_validate(
        choice_response_contact_message_data
    )

    assert isinstance(parsed_response, ChoiceResponseContactMessage)
    assert parsed_response.choice_response_message is not None
    assert parsed_response.choice_response_message.message_id == "message id value"
    assert parsed_response.choice_response_message.postback_data == "postback data value"
    assert parsed_response.reply_to is not None
