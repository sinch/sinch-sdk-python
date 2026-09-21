import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)


def test_app_id_request_expects_parsed_input():
    """Test that the model correctly parses a valid app_id."""
    model = AppIdRequest(app_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert model.app_id == "01FC66621XXXXX119Z8PMV1QPQ"


def test_app_id_request_expects_validation_error_for_missing_app_id():
    """Test that a ValidationError is raised when the required app_id is missing."""
    with pytest.raises(ValidationError) as excinfo:
        AppIdRequest()

    assert "app_id" in str(excinfo.value)
