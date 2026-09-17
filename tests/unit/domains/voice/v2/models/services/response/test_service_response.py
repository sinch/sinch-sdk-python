import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    EventDestinationCallBehavior,
)


def test_service_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ServiceResponse(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        create_time="2025-01-01T00:00:00Z",
        update_time="2025-06-01T09:15:00Z",
        name="My Voice Service",
        description="Service with custom event call behavior",
        is_default=True,
        call_behavior={
            "type": "WEBHOOK",
            "webhook": {
                "url": "https://example.com/event_destination",
                "fallback_url": "https://example.com/fallback",
            },
            
        },
    )

    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert model.create_time is not None
    assert model.update_time is not None
    assert model.name == "My Voice Service"
    assert model.description == "Service with custom event call behavior"
    assert model.is_default is True
    assert isinstance(model.call_behavior, EventDestinationCallBehavior)
    assert model.call_behavior.type == "EVENT_DESTINATION"
    assert model.call_behavior.event_destination.url == "https://example.com/event_destination"
    assert model.call_behavior.event_destination.fallback_url == "https://example.com/fallback"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert alias_dump["createTime"] == "2025-01-01T00:00:00Z"
    assert alias_dump["updateTime"] == "2025-06-01T09:15:00Z"
    assert alias_dump["name"] == "My Voice Service"
    assert alias_dump["isDefault"] is True
    assert alias_dump["callBehavior"]["type"] == "WEBHOOK"
    assert alias_dump["callBehavior"]["webhook"]["url"] == "https://example.com/event_destination"
    assert alias_dump["callBehavior"]["webhook"]["fallbackUrl"] == "https://example.com/fallback"


def test_service_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ServiceResponse(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        create_time="2025-01-01T00:00:00Z",
        name="My Voice Service",
        is_default=False,
    )

    assert model.update_time is None
    assert model.description is None
    assert model.call_behavior is None


def test_service_response_expects_validation_error_for_missing_required():
    """Test that required fields raise a validation error when missing."""
    with pytest.raises(ValidationError):
        ServiceResponse()
