from pydantic import TypeAdapter, ValidationError
import pytest

from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    CallBehavior,
    NoneCallBehavior,
    StaticCallBehavior,
    EventDestinationCallBehavior,
)


def test_none_call_behavior_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = NoneCallBehavior(type="NONE")

    assert model.type == "NONE"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["type"] == "NONE"


def test_event_destination_call_behavior_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDestinationCallBehavior(
        type="EVENT_DESTINATION",
        event_destination={"url": "https://example.com/event_destination"},
    )

    assert model.type == "EVENT_DESTINATION"
    assert model.event_destination.url == "https://example.com/event_destination"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["type"] == "WEBHOOK"
    assert alias_dump["webhook"]["url"] == "https://example.com/event_destination"


def test_static_call_behavior_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StaticCallBehavior(
        type="STATIC",
        static={"commands": [{"command": "hangup"}]},
    )

    assert model.type == "STATIC"
    assert model.static.commands[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["type"] == "STATIC"
    assert alias_dump["static"]["commands"][0]["command"] == "hangup"


def test_call_behavior_expects_each_variant_resolved_by_discriminator():
    """Test that each oneOf variant is resolved from its type discriminator."""
    adapter = TypeAdapter(CallBehavior)

    none_behavior = adapter.validate_python({"type": "NONE"})
    custom_event_behavior = adapter.validate_python(
        {"type": "EVENT_DESTINATION", "event_destination": {"url": "https://example.com/event_destination"}}
    )
    static_behavior = adapter.validate_python(
        {"type": "STATIC", "static": {"commands": [{"command": "hangup"}]}}
    )

    assert pytest.raises(ValidationError, lambda: adapter.validate_python({"type": "WEBHOOK"}))
    assert pytest.raises(ValidationError, lambda: adapter.validate_python({"type": "INVALID"}))
    assert isinstance(none_behavior, NoneCallBehavior)
    assert isinstance(custom_event_behavior, EventDestinationCallBehavior)
    assert isinstance(static_behavior, StaticCallBehavior)

