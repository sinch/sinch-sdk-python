from sinch.domains.voice.models.v2.services.internal.request.create_service_request import (
    CreateServiceRequest,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    EventDestinationCallBehavior,
)


def test_create_service_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CreateServiceRequest(
        name="Example service",
        description="Service with custom events",
        is_default=True,
        call_behavior={
            "type": "EVENT_DESTINATION",
            "event_destination": {"url": "https://example.com/event_destination"},
        },
        idempotency_key="my-custom-key",
    )

    assert model.name == "Example service"
    assert model.description == "Service with custom events"
    assert model.is_default is True
    assert isinstance(model.call_behavior, EventDestinationCallBehavior)
    assert model.call_behavior.event_destination.url == "https://example.com/event_destination"
    assert model.idempotency_key == "my-custom-key"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["name"] == "Example service"
    assert alias_dump["description"] == "Service with custom events"
    assert alias_dump["isDefault"] is True
    assert alias_dump["callBehavior"]["type"] == "WEBHOOK"
    assert alias_dump["callBehavior"]["webhook"]["url"] == (
        "https://example.com/event_destination"
    )
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_create_service_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = CreateServiceRequest(name="Example service")

    assert model.description is None
    assert model.is_default is None
    assert model.call_behavior is None
