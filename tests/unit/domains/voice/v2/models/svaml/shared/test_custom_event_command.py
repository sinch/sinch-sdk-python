import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.custom_event_command import (
    CustomEventCommand,
)


def test_custom_event_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CustomEventCommand(
        command="customEvent",
        custom_event_name="my.custom.event",
        url="https://example.com/eventDestination",
        fallback_url="https://example.com/fallback",
    )

    assert model.command == "customEvent"
    assert model.custom_event_name == "my.custom.event"
    assert model.url == "https://example.com/eventDestination"
    assert model.fallback_url == "https://example.com/fallback"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["webhookName"] == "my.custom.event"
    assert alias_dump["fallbackUrl"] == "https://example.com/fallback"
    assert alias_dump["command"] == "webhook"


def test_custom_event_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = CustomEventCommand(
        command="customEvent",
        custom_event_name="my.custom.event",
        url="https://example.com/eventDestination",
    )

    assert model.fallback_url is None


def test_custom_event_command_expects_validation_error_for_missing_required():
    """Test that customEvent_name and url are required."""
    with pytest.raises(ValidationError):
        CustomEventCommand(command="customEvent")


def test_custom_event_command_serializes_command_as_wire_value():
    """Test that the model always dumps "webhook" for the server, regardless of the SDK-facing command value."""
    model = CustomEventCommand(
        command="customEvent",
        custom_event_name="my.custom.event",
        url="https://example.com/eventDestination",
    )

    alias_dump = model.model_dump(by_alias=True)
    assert alias_dump["command"] == "webhook"


def test_custom_event_command_accepts_wire_command_value():
    """Test that a "webhook" command value coming from the API is normalized to "customEvent"."""
    model = CustomEventCommand.model_validate(
        {
            "command": "webhook",
            "webhookName": "my.custom.event",
            "url": "https://example.com/eventDestination",
        }
    )

    assert model.command == "customEvent"
