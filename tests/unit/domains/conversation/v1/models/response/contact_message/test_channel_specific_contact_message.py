import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    ChannelSpecificContactMessage,
)


@pytest.fixture
def channel_specific_contact_message_data():
    return {
        "channel_specific_message": {
            "message_type": "nfm_reply",
            "message": {
                "type": "nfm_reply",
                "nfm_reply": {
                    "name": "address_message",
                    "response_json": "{\"key\": \"value\"}",
                    "body": "nfm reply body value"
                }
            }
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_channel_specific_contact_message_expects_correct_fields(
    channel_specific_contact_message_data,
):
    """Test that ChannelSpecificContactMessage is parsed correctly with all fields."""
    parsed_response = ChannelSpecificContactMessage.model_validate(
        channel_specific_contact_message_data
    )

    assert isinstance(parsed_response, ChannelSpecificContactMessage)
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.channel_specific_message.message_type == "nfm_reply"
    assert parsed_response.channel_specific_message.message is not None
    assert parsed_response.channel_specific_message.message.type == "nfm_reply"
    assert parsed_response.channel_specific_message.message.nfm_reply is not None
    assert parsed_response.channel_specific_message.message.nfm_reply.name == "address_message"
    assert parsed_response.channel_specific_message.message.nfm_reply.response_json == "{\"key\": \"value\"}"
    assert parsed_response.channel_specific_message.message.nfm_reply.body == "nfm reply body value"
    assert parsed_response.reply_to is not None
    assert parsed_response.reply_to.message_id == "message id value"
