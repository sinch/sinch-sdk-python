import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)


def test_start_call_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StartCallResponse(
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC",
    )

    assert model.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert model.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert model.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert alias_dump["batchId"] == "01BX5ZZKBKACTAV9WEVGEMMVRC"


def test_start_call_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = StartCallResponse(
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
    )

    assert model.session_id is None
    assert model.batch_id is None


def test_start_call_response_expects_validation_error_for_missing_required():
    """Test that project_id and service_id are required."""
    with pytest.raises(ValidationError):
        StartCallResponse()
