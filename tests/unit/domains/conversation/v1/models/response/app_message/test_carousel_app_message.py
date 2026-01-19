import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    CarouselAppMessage,
)


@pytest.fixture
def carousel_app_message_data():
    """Test data for CarouselAppMessage from Java SDK."""
    return {
        "carousel_message": {
            "cards": [
                {
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
                        }
                    ]
                }
            ],
            "choices": [
                {
                    "call_message": {
                        "title": "title value",
                        "phone_number": "phone number value"
                    },
                    "postback_data": "postback call_message data value"
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


def test_parsing_carousel_app_message_expects_correct_fields(carousel_app_message_data):
    """Test that CarouselAppMessage is parsed correctly with all fields."""
    parsed_response = CarouselAppMessage.model_validate(carousel_app_message_data)

    assert isinstance(parsed_response, CarouselAppMessage)
    assert parsed_response.carousel_message is not None
    assert len(parsed_response.carousel_message.cards) == 1
    assert parsed_response.carousel_message.cards[0].title == "title value"
    assert parsed_response.carousel_message.cards[0].description == "description value"
    assert parsed_response.carousel_message.cards[0].height == "MEDIUM"
    assert len(parsed_response.carousel_message.choices) == 1
    assert parsed_response.carousel_message.choices[0].call_message.title == "title value"
    assert parsed_response.carousel_message.choices[0].call_message.phone_number == "phone number value"
    assert parsed_response.carousel_message.choices[0].postback_data == "postback call_message data value"
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
