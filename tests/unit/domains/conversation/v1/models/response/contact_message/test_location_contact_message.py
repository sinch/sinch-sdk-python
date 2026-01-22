import pytest
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    LocationContactMessage,
)


@pytest.fixture
def location_contact_message_data():
    return {
        "location_message": {
            "coordinates": {
                "latitude": 47.6279809,
                "longitude": -2.8229159
            },
            "label": "label value",
            "title": "title value"
        },
        "reply_to": {
            "message_id": "message id value"
        }
    }


def test_parsing_location_contact_message_expects_correct_fields(
    location_contact_message_data,
):
    """Test that LocationContactMessage is parsed correctly with all fields."""
    parsed_response = LocationContactMessage.model_validate(
        location_contact_message_data
    )

    assert isinstance(parsed_response, LocationContactMessage)
    assert parsed_response.location_message is not None
    assert parsed_response.location_message.coordinates.latitude == 47.6279809
    assert parsed_response.location_message.coordinates.longitude == -2.8229159
    assert parsed_response.location_message.label == "label value"
    assert parsed_response.location_message.title == "title value"
    assert parsed_response.reply_to is not None
