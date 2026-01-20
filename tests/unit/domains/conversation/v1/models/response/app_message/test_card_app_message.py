import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    CardAppMessage,
)


@pytest.fixture
def card_app_message_data():
    """Test data for CardAppMessage from Java SDK."""
    return {
        "card_message": {
            "title": "title value",
            "description": "description value",
            "media_message": {
                "url": "an url value",
                "thumbnail_url": "another url",
                "filename_override": "filename override value"
            },
            "height": "MEDIUM",
            "choices": [
                {
                    "text_message": {
                        "text": "This is a text message."
                    },
                    "postback_data": "postback_data text"
                },
                {
                    "call_message": {
                        "title": "title value",
                        "phone_number": "phone number value"
                    },
                    "postback_data": "postback_data call"
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
                    "postback_data": "postback_data location"
                },
                {
                    "url_message": {
                        "title": "title value",
                        "url": "an url value"
                    },
                    "postback_data": "postback_data url"
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


def test_parsing_card_app_message_expects_correct_fields(card_app_message_data):
    """Test that CardAppMessage is parsed correctly with all fields."""
    parsed_response = CardAppMessage.model_validate(card_app_message_data)

    assert isinstance(parsed_response, CardAppMessage)
    assert parsed_response.card_message is not None
    assert parsed_response.card_message.title == "title value"
    assert parsed_response.card_message.description == "description value"
    assert parsed_response.card_message.height == "MEDIUM"
    assert parsed_response.card_message.media_message is not None
    assert parsed_response.card_message.media_message.url == "an url value"
    assert parsed_response.card_message.media_message.thumbnail_url == "another url"
    assert parsed_response.card_message.media_message.filename_override == "filename override value"
    assert len(parsed_response.card_message.choices) == 6
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.agent is not None
