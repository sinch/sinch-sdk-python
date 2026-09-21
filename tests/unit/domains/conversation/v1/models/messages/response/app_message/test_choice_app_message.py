import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    ChoiceAppMessage,
)


@pytest.fixture
def choice_app_message_data():
    return {
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
                },
                {
                    "location_message": {
                        "coordinates": {
                            "latitude": 47.6279809,
                            "longitude": -2.8229159
                        },
                        "title": "title value",
                        "label": "label value"
                    },
                    "postback_data": "postback location_message data value"
                },
                {
                    "text_message": {
                        "text": "This is a text message."
                    },
                    "postback_data": "postback text_message data value"
                },
                {
                    "url_message": {
                        "title": "title value",
                        "url": "an url value"
                    },
                    "postback_data": "postback url_message data value"
                },
                {
                    "calendar_message": {
                        "title": "Calendar Message Example",
                        "event_start": "2023-10-01T10:00:00Z",
                        "event_end": "2023-10-01T11:00:00Z",
                        "event_title": "Team Meeting",
                        "event_description": "Monthly team sync-up",
                        "fallback_url": "https://calendar.example.com/event/12345"
                    },
                    "postback_data": "postback calendar_message data value"
                },
                {
                    "share_location_message": {
                        "title": "Share Location Example",
                        "fallback_url": "https://maps.example.com/?q=37.7749,-122.4194"
                    },
                    "postback_data": "postback share_location_message data value"
                }
            ]
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


def test_parsing_choice_app_message_expects_correct_fields(choice_app_message_data):
    """Test that ChoiceAppMessage is parsed correctly with all fields."""
    parsed_response = ChoiceAppMessage.model_validate(choice_app_message_data)

    assert isinstance(parsed_response, ChoiceAppMessage)
    assert parsed_response.choice_message is not None
    assert parsed_response.choice_message.text_message is not None
    assert parsed_response.choice_message.text_message.text == "This is a text message."
    assert len(parsed_response.choice_message.choices) == 6
    assert parsed_response.choice_message.choices[0].call_message.title == "title value"
    assert parsed_response.choice_message.choices[0].call_message.phone_number == "phone number value"
    assert parsed_response.choice_message.choices[0].postback_data == "postback call_message data value"
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
