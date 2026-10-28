import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.shared.generic_event import (
    GenericEvent,
)


def test_generic_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = GenericEvent(payload={"key": "value", "nested": {"count": 1}})

    assert model.payload == {"key": "value", "nested": {"count": 1}}

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump == {"payload": {"key": "value", "nested": {"count": 1}}}


def test_generic_event_expects_empty_payload_accepted():
    """Test that an empty JSON object is a valid payload."""
    assert GenericEvent(payload={}).payload == {}


def test_generic_event_expects_validation_error_for_missing_required():
    """Test that payload is required."""
    with pytest.raises(ValidationError):
        GenericEvent()
