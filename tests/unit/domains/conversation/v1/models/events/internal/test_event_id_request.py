import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.internal.event_id_request import (
    EventIdRequest,
)


def test_event_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventIdRequest(event_id="01W4FFL35P4NC4K35EVENT0001")

    assert model.event_id == "01W4FFL35P4NC4K35EVENT0001"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["event_id"] == "01W4FFL35P4NC4K35EVENT0001"


def test_event_id_request_expects_validation_error_for_missing_required():
    """Test that event_id is required."""
    with pytest.raises(ValidationError):
        EventIdRequest()
