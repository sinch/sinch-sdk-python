import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal.inbound_id_request import InboundIdRequest


def test_inbound_id_request_expects_valid_inbound_id():
    """Test that the model correctly parses a valid inbound ID."""
    model = InboundIdRequest(inbound_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert model.inbound_id == "01FC66621XXXXX119Z8PMV1QPQ"


def test_inbound_id_request_expects_validation_error_for_missing_inbound_id():
    """Test that missing required inbound_id field raises a ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        InboundIdRequest()

    assert "inbound_id" in str(exc_info.value)
