from sinch.domains.voice.models.v2.services.internal.request.update_service_request import (
    UpdateServiceRequest,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    NoneCallBehavior,
)


def test_update_service_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UpdateServiceRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        name="Renamed service",
        description="Updated description",
        is_default=True,
        call_behavior={"type": "NONE"},
        idempotency_key="my-custom-key",
    )

    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.name == "Renamed service"
    assert model.description == "Updated description"
    assert model.is_default is True
    assert isinstance(model.call_behavior, NoneCallBehavior)
    assert model.idempotency_key == "my-custom-key"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["name"] == "Renamed service"
    assert alias_dump["description"] == "Updated description"
    assert alias_dump["isDefault"] is True
    assert alias_dump["callBehavior"] == {"type": "NONE"}
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_update_service_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = UpdateServiceRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade"
    )

    assert model.name is None
    assert model.description is None
    assert model.is_default is None
    assert model.call_behavior is None
