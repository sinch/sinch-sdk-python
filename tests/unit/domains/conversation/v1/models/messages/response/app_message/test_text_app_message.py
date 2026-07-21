import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TextAppMessage,
)


@pytest.fixture
def text_app_message_data():
    return {
        "text_message": {
            "text": "This is a text message."
        },
        "explicit_channel_message": {
            "KAKAOTALK": "foo value"
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "choice_message": {
                    "text_message": {
                        "text": "This is a text message."
                    },
                    "choices": [
                        {
                            "call_message": {
                                "title": "title value",
                                "phone_number": "phone number value"
                            },
                            "postback_data": "postback call_message data value"
                        }
                    ]
                }
            }
        },
        "channel_specific_message": {
            "MESSENGER": {
                "message_type": "FLOWS",
                "message": {
                    "flow_id": "1",
                    "flow_cta": "Book!",
                    "header": {
                        "type": "text",
                        "text": "text header value"
                    },
                    "body": {
                        "text": "Flow message body"
                    },
                    "footer": {
                        "text": "Flow message footer"
                    },
                    "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s.",
                    "flow_mode": "draft",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "<SCREEN_NAME>",
                        "data": {
                            "product_name": "name",
                            "product_description": "description",
                            "product_price": 100
                        }
                    }
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_text_app_message_expects_correct_fields(text_app_message_data):
    """Test that TextAppMessage is parsed correctly with all fields."""
    parsed_response = TextAppMessage.model_validate(text_app_message_data)

    assert isinstance(parsed_response, TextAppMessage)
    assert parsed_response.text_message is not None
    assert parsed_response.text_message.text == "This is a text message."
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.agent is not None
