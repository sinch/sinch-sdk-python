from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.shared import MOBinaryMessage


@pytest.fixture
def sample_mo_binary_data():
    return {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "body": "SGVsbG8gV29ybGQ=",
        "udh": "050003010201",
        "type": "mo_binary",
        "received_at": "2024-06-06T09:22:14.304Z",
    }


def test_mo_binary_message_expects_valid_input(sample_mo_binary_data):
    """Test that the model correctly parses valid input."""
    msg = MOBinaryMessage(**sample_mo_binary_data)

    assert msg.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert msg.from_ == "+46701234567"
    assert msg.to == "+46709876543"
    assert msg.body == "SGVsbG8gV29ybGQ="
    assert msg.udh == "050003010201"
    assert msg.type == "mo_binary"
    assert msg.received_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)


def test_mo_binary_message_expects_optional_fields_none(sample_mo_binary_data):
    """Test that optional fields default to None when not provided."""
    msg = MOBinaryMessage(**sample_mo_binary_data)

    assert msg.client_reference is None
    assert msg.operator_id is None
    assert msg.sent_at is None


def test_mo_binary_message_expects_optional_fields_populated():
    """Test that optional fields are parsed correctly when provided."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "body": "SGVsbG8gV29ybGQ=",
        "udh": "050003010201",
        "type": "mo_binary",
        "received_at": "2024-06-06T09:22:14.304Z",
        "client_reference": "my-client-ref",
        "operator_id": "24001",
    }
    msg = MOBinaryMessage(**data)

    assert msg.client_reference == "my-client-ref"
    assert msg.operator_id == "24001"


def test_mo_binary_message_expects_validation_error_for_missing_udh():
    """Test that missing required udh field raises a ValidationError."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "body": "SGVsbG8gV29ybGQ=",
        "type": "mo_binary",
        "received_at": "2024-06-06T09:22:14.304Z",
    }
    with pytest.raises(ValidationError) as exc_info:
        MOBinaryMessage(**data)

    assert "udh" in str(exc_info.value)


def test_mo_binary_message_expects_validation_error_for_missing_body():
    """Test that missing required body field raises a ValidationError."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "udh": "050003010201",
        "type": "mo_binary",
        "received_at": "2024-06-06T09:22:14.304Z",
    }
    with pytest.raises(ValidationError) as exc_info:
        MOBinaryMessage(**data)

    assert "body" in str(exc_info.value)
