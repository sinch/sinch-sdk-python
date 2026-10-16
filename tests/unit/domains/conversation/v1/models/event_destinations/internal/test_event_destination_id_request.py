import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.event_destinations.internal.event_destination_id_request import (
    EventDestinationIdRequest,
)


def test_event_destination_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDestinationIdRequest(
        event_destination_id="01W4FFL35P4NC4K35WEBHOOK001"
    )

    assert model.event_destination_id == "01W4FFL35P4NC4K35WEBHOOK001"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["event_destination_id"] == "01W4FFL35P4NC4K35WEBHOOK001"


def test_event_destination_id_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        EventDestinationIdRequest()
