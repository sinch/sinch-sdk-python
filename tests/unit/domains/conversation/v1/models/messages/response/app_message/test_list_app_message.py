import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    ListAppMessage,
)


@pytest.fixture
def list_app_message_data():
    return {
        "list_message": {
            "title": "a list message title value",
            "sections": [
                {
                    "title": "a list section title value",
                    "items": [
                        {
                            "choice": {
                                "title": "choice title",
                                "description": "description value",
                                "media": {
                                    "url": "an url value",
                                    "thumbnail_url": "another url",
                                    "filename_override": "filename override value"
                                },
                                "postback_data": "postback value"
                            }
                        }
                    ]
                }
            ],
            "description": "description value",
            "message_properties": {
                "catalog_id": "catalog ID value",
                "menu": "menu value"
            },
            "media": {
                "url": "an url value",
                "thumbnail_url": "another url",
                "filename_override": "filename override value"
            }
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


def test_parsing_list_app_message_expects_correct_fields(list_app_message_data):
    """Test that ListAppMessage is parsed correctly with all fields."""
    parsed_response = ListAppMessage.model_validate(list_app_message_data)

    assert isinstance(parsed_response, ListAppMessage)
    assert parsed_response.list_message is not None
    assert parsed_response.list_message.title == "a list message title value"
    assert parsed_response.list_message.description == "description value"
    assert len(parsed_response.list_message.sections) == 1
    assert parsed_response.list_message.sections[0].title == "a list section title value"
    assert len(parsed_response.list_message.sections[0].items) == 1
    assert parsed_response.list_message.sections[0].items[0].choice.title == "choice title"
    assert parsed_response.list_message.sections[0].items[0].choice.description == "description value"
    assert parsed_response.list_message.message_properties is not None
    assert parsed_response.list_message.message_properties.catalog_id == "catalog ID value"
    assert parsed_response.list_message.message_properties.menu == "menu value"
    assert parsed_response.list_message.media is not None
    assert parsed_response.list_message.media.url == "an url value"
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
