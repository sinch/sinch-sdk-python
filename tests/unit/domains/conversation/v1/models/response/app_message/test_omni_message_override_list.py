import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    ListAppMessage,
)


@pytest.fixture
def list_app_message_with_omni_override_list_data():
    return {
        "list_message": {
            "title": "a list message title value",
            "sections": [
                {
                    "title": "a list section title value",
                    "items": [
                        {
                            "product": {
                                "id": "product ID value",
                                "marketplace": "marketplace value",
                                "quantity": 4,
                                "item_price": 3.14159,
                                "currency": "currency value"
                            }
                        }
                    ]
                }
            ]
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "list_message": {
                    "title": "a list message title value",
                    "sections": [
                        {
                            "title": "a list section title value",
                            "items": [
                                {
                                    "product": {
                                        "id": "product ID value",
                                        "marketplace": "marketplace value",
                                        "quantity": 4,
                                        "item_price": 3.14159,
                                        "currency": "currency value"
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
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_list_app_message_with_omni_override_list_expects_correct_fields(
    list_app_message_with_omni_override_list_data,
):
    """Test that ListAppMessage with OmniMessageOverrideList is parsed correctly."""
    parsed_response = ListAppMessage.model_validate(
        list_app_message_with_omni_override_list_data
    )

    assert isinstance(parsed_response, ListAppMessage)
    assert parsed_response.list_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.list_message is not None
    assert omni_override.list_message.title == "a list message title value"
    assert len(omni_override.list_message.sections) == 1
    assert omni_override.list_message.description == "description value"
    assert omni_override.list_message.message_properties is not None
    assert omni_override.list_message.message_properties.catalog_id == "catalog ID value"
    assert omni_override.list_message.message_properties.menu == "menu value"
    assert omni_override.list_message.media is not None
    assert parsed_response.agent is not None
