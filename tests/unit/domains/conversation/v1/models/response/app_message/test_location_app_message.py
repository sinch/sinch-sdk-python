import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    LocationAppMessage,
)


@pytest.fixture
def location_app_message_data():
    return {
        "location_message": {
            "coordinates": {
                "latitude": 47.6279809,
                "longitude": -2.8229159
            },
            "label": "label value",
            "title": "title value"
        },
        "explicit_channel_message": {
            "KAKAOTALK": "foo value"
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "choice_message": {
                    "choices": [
                        {
                            "call_message": {
                                "phone_number": "phone number value",
                                "title": "title value"
                            },
                            "postback_data": "postback call_message data value"
                        }
                    ],
                    "text_message": {
                        "text": "This is a text message."
                    }
                }
            }
        },
        "channel_specific_message": {
            "MESSENGER": {
                "message_type": "FLOWS",
                "message": {
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
                    "flow_id": "1",
                    "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s.",
                    "flow_mode": "draft",
                    "flow_cta": "Book!",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "<SCREEN_NAME>",
                        "data": {
                            "product_price": 100,
                            "product_description": "description",
                            "product_name": "name"
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


def test_parsing_location_app_message_expects_correct_fields(location_app_message_data):
    """Test that LocationAppMessage is parsed correctly with all fields."""
    parsed_response = LocationAppMessage.model_validate(location_app_message_data)

    assert isinstance(parsed_response, LocationAppMessage)
    assert parsed_response.location_message is not None
    assert parsed_response.location_message.title == "title value"
    assert parsed_response.location_message.label == "label value"
    assert parsed_response.location_message.coordinates.latitude == 47.6279809
    assert parsed_response.location_message.coordinates.longitude == -2.8229159
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
