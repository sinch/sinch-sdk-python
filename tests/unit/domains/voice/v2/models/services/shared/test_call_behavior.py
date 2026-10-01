from pydantic import TypeAdapter, ValidationError
import pytest

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse

from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    CallBehavior,
    NoneCallBehavior,
    StaticCallBehavior,
    EventDestinationCallBehavior,
)


adapter = TypeAdapter(CallBehavior)


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


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"type": "NONE"}, NoneCallBehavior),
        (
            {
                "type": "EVENT_DESTINATION",
                "event_destination": {
                    "url": "https://example.com/event_destination"
                },
            },
            EventDestinationCallBehavior,
        ),
        (
            {"type": "STATIC", "static": {"commands": [{"command": "hangup"}]}},
            StaticCallBehavior,
        ),
    ],
    ids=["none", "event_destination", "static"],
)
def test_call_behavior_expects_each_variant_resolved(payload, expected_model):
    """Test that each oneOf variant is resolved from its type discriminator."""
    assert type(adapter.validate_python(payload)) is expected_model


@pytest.mark.parametrize(
    "payload",
    [{"type": "WEBHOOK"}, {"type": "INVALID"}],
    ids=["unknown_type", "invalid_type"],
)
def test_call_behavior_expects_validation_error_on_unknown_type(payload):
    """Test that a type the SDK does not know is rejected when a service is
    being configured."""
    with pytest.raises(ValidationError, match="does not match any of the expected tags"):
        adapter.validate_python(payload)


def test_call_behavior_expects_validation_error_on_missing_type():
    """Test that a call behavior without a type is rejected."""
    with pytest.raises(ValidationError, match="Unable to extract tag"):
        adapter.validate_python({})


def test_call_behavior_expects_unknown_type_parsed_in_a_response():
    """Test that a behavior added to the API later is parsed as SinchRawResponse
    instead of failing the whole service response."""
    payload = {"type": "WEBHOOK", "webhook": {"url": "https://example.com"}}

    with response_parsing_scope():
        behavior = adapter.validate_python(payload)

    assert isinstance(behavior, SinchRawResponse)
    assert behavior.model_dump() == payload
