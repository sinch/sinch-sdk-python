import pytest
from datetime import date
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    ContactInfoAppMessage,
)


@pytest.fixture
def contact_info_app_message_with_omni_override_contact_info_data():
    return {
        "contact_info_message": {
            "name": {
                "full_name": "full_name value",
                "first_name": "first_name value",
                "last_name": "last_name value"
            },
            "phone_numbers": []
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
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
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_contact_info_app_message_with_omni_override_contact_info_expects_correct_fields(
    contact_info_app_message_with_omni_override_contact_info_data,
):
    """Test that ContactInfoAppMessage with OmniMessageOverrideContactInfo is parsed correctly."""
    parsed_response = ContactInfoAppMessage.model_validate(
        contact_info_app_message_with_omni_override_contact_info_data
    )

    assert isinstance(parsed_response, ContactInfoAppMessage)
    assert parsed_response.contact_info_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.contact_info_message is not None
    assert omni_override.contact_info_message.name.full_name == "full_name value"
    assert omni_override.contact_info_message.name.first_name == "first_name value"
    assert omni_override.contact_info_message.name.last_name == "last_name value"
    assert omni_override.contact_info_message.name.middle_name == "middle_name value"
    assert omni_override.contact_info_message.name.prefix == "prefix value"
    assert omni_override.contact_info_message.name.suffix == "suffix value"
    assert len(omni_override.contact_info_message.phone_numbers) == 1
    assert len(omni_override.contact_info_message.addresses) == 1
    assert len(omni_override.contact_info_message.email_addresses) == 1
    assert omni_override.contact_info_message.organization is not None
    assert len(omni_override.contact_info_message.urls) == 1
    assert isinstance(omni_override.contact_info_message.birthday, date)
    assert omni_override.contact_info_message.birthday == date(1968, 7, 7)
    assert parsed_response.agent is not None
