import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.services.response.service_short_response import (
    ServiceShortResponse,
)


def test_service_short_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ServiceShortResponse(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        create_time="2025-01-01T00:00:00Z",
        update_time="2025-02-15T10:30:00Z",
        name="Primary Service",
        description="Main service",
        is_default=True,
    )

    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert model.create_time is not None
    assert model.update_time is not None
    assert model.name == "Primary Service"
    assert model.description == "Main service"
    assert model.is_default is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert alias_dump["createTime"] == "2025-01-01T00:00:00Z"
    assert alias_dump["updateTime"] == "2025-02-15T10:30:00Z"
    assert alias_dump["name"] == "Primary Service"
    assert alias_dump["isDefault"] is True
    assert alias_dump["description"] == "Main service"


def test_service_short_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ServiceShortResponse(
        service_id="7f235289-d3ae-57b6-a54d-6d3bf655bbdf",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        create_time="2025-02-15T10:30:00Z",
        name="Secondary Service",
        is_default=False,
    )

    assert model.update_time is None
    assert model.description is None


def test_service_short_response_expects_validation_error_for_missing_required():
    """Test that required fields raise a validation error when missing."""
    with pytest.raises(ValidationError):
        ServiceShortResponse()
