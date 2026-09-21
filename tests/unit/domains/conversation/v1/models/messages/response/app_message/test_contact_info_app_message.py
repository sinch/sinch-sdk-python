import pytest
from datetime import date
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    ContactInfoAppMessage,
)


@pytest.fixture
def contact_info_app_message_data():
    return {
        "contact_info_message": {
            "name": {
                "full_name": "full_name value",
                "first_name": "first_name value",
                "last_name": "last_name value",
                "middle_name": "middle_name value",
                "prefix": "prefix value",
                "suffix": "suffix value"
            },
            "phone_numbers": [
                {
                    "phone_number": "phone_number value",
                    "type": "type value"
                }
            ],
            "addresses": [
                {
                    "city": "city value",
                    "country": "country value",
                    "state": "state va@lue",
                    "zip": "zip value",
                    "country_code": "country_code value"
                }
            ],
            "email_addresses": [
                {
                    "email_address": "email_address value",
                    "type": "type value"
                }
            ],
            "organization": {
                "company": "company value",
                "department": "department value",
                "title": "title value"
            },
            "urls": [
                {
                    "url": "url value",
                    "type": "type value"
                }
            ],
            "birthday": "1968-07-07"
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


def test_parsing_contact_info_app_message_expects_correct_fields(contact_info_app_message_data):
    """Test that ContactInfoAppMessage is parsed correctly with all fields."""
    parsed_response = ContactInfoAppMessage.model_validate(contact_info_app_message_data)

    assert isinstance(parsed_response, ContactInfoAppMessage)
    assert parsed_response.contact_info_message is not None
    assert parsed_response.contact_info_message.name is not None
    assert parsed_response.contact_info_message.name.full_name == "full_name value"
    assert parsed_response.contact_info_message.name.first_name == "first_name value"
    assert parsed_response.contact_info_message.name.last_name == "last_name value"
    assert parsed_response.contact_info_message.name.middle_name == "middle_name value"
    assert parsed_response.contact_info_message.name.prefix == "prefix value"
    assert parsed_response.contact_info_message.name.suffix == "suffix value"
    assert len(parsed_response.contact_info_message.phone_numbers) == 1
    assert parsed_response.contact_info_message.phone_numbers[0].phone_number == "phone_number value"
    assert parsed_response.contact_info_message.phone_numbers[0].type == "type value"
    assert len(parsed_response.contact_info_message.addresses) == 1
    assert len(parsed_response.contact_info_message.email_addresses) == 1
    assert parsed_response.contact_info_message.organization is not None
    assert len(parsed_response.contact_info_message.urls) == 1
    assert isinstance(parsed_response.contact_info_message.birthday, date)
    assert parsed_response.contact_info_message.birthday == date(1968, 7, 7)
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.agent is not None
