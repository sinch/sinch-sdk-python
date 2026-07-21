import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    CarouselAppMessage,
)


@pytest.fixture
def carousel_app_message_with_omni_override_carousel_data():
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
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
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
                        }
                    ],
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
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_carousel_app_message_with_omni_override_carousel_expects_correct_fields(
    carousel_app_message_with_omni_override_carousel_data,
):
    """Test that CarouselAppMessage with OmniMessageOverrideCarousel is parsed correctly."""
    parsed_response = CarouselAppMessage.model_validate(
        carousel_app_message_with_omni_override_carousel_data
    )

    assert isinstance(parsed_response, CarouselAppMessage)
    assert parsed_response.carousel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.carousel_message is not None
    assert len(omni_override.carousel_message.cards) == 1
    assert len(omni_override.carousel_message.choices) == 6
    assert parsed_response.agent is not None
