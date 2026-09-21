import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    LocationAppMessage,
)


@pytest.fixture
def location_app_message_with_omni_override_location_data():
    return {
        "location_message": {
            "coordinates": {
                "latitude": 47.6279809,
                "longitude": -2.8229159
            },
            "title": "title value",
            "label": "label value"
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "location_message": {
                    "coordinates": {
                        "latitude": 47.6279809,
                        "longitude": -2.8229159
                    },
                    "title": "title value",
                    "label": "label value"
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_location_app_message_with_omni_override_location_expects_correct_fields(
    location_app_message_with_omni_override_location_data,
):
    """Test that LocationAppMessage with OmniMessageOverrideLocation is parsed correctly."""
    parsed_response = LocationAppMessage.model_validate(
        location_app_message_with_omni_override_location_data
    )

    assert isinstance(parsed_response, LocationAppMessage)
    assert parsed_response.location_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.location_message is not None
    assert omni_override.location_message.coordinates.latitude == 47.6279809
    assert omni_override.location_message.coordinates.longitude == -2.8229159
    assert omni_override.location_message.title == "title value"
    assert omni_override.location_message.label == "label value"
    assert parsed_response.agent is not None
