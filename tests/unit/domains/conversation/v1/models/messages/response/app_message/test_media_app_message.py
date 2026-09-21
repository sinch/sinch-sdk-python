import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    MediaAppMessage,
)


@pytest.fixture
def media_app_message_data():
    return {
        "media_message": {
            "url": "an url value",
            "thumbnail_url": "another url",
            "filename_override": "filename override value"
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


def test_parsing_media_app_message_expects_correct_fields(media_app_message_data):
    """Test that MediaAppMessage is parsed correctly with all fields."""
    parsed_response = MediaAppMessage.model_validate(media_app_message_data)

    assert isinstance(parsed_response, MediaAppMessage)
    assert parsed_response.media_message is not None
    assert parsed_response.media_message.url == "an url value"
    assert parsed_response.media_message.thumbnail_url == "another url"
    assert parsed_response.media_message.filename_override == "filename override value"
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
