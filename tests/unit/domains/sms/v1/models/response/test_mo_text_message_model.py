from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.shared import MOTextMessage


@pytest.fixture
def sample_mo_text_data():
    return {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "body": "Hello world",
        "type": "mo_text",
        "received_at": "2024-06-06T09:22:14.304Z",
    }


def test_mo_text_message_expects_valid_input(sample_mo_text_data):
    """Test that the model correctly parses valid input."""
    msg = MOTextMessage(**sample_mo_text_data)

    assert msg.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert msg.from_ == "+46701234567"
    assert msg.to == "+46709876543"
    assert msg.body == "Hello world"
    assert msg.type == "mo_text"
    assert msg.received_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)


def test_mo_text_message_expects_optional_fields_none(sample_mo_text_data):
    """Test that optional fields default to None when not provided."""
    msg = MOTextMessage(**sample_mo_text_data)

    assert msg.client_reference is None
    assert msg.operator_id is None
    assert msg.sent_at is None


def test_mo_text_message_expects_from_alias(sample_mo_text_data):
    """Test that the model accepts 'from' alias and exposes it as 'from_'."""
    msg = MOTextMessage(**sample_mo_text_data)

    assert msg.from_ == "+46701234567"


def test_mo_text_message_expects_optional_fields_populated():
    """Test that optional fields are parsed correctly when provided."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "body": "Hello world",
        "type": "mo_text",
        "received_at": "2024-06-06T09:22:14.304Z",
        "client_reference": "my-client-ref",
        "operator_id": "24001",
        "sent_at": "2024-06-06T09:20:00.000Z",
    }
    msg = MOTextMessage(**data)

    assert msg.client_reference == "my-client-ref"
    assert msg.operator_id == "24001"
    assert msg.sent_at == datetime(2024, 6, 6, 9, 20, 0, tzinfo=timezone.utc)


def test_mo_text_message_expects_validation_error_for_missing_body():
    """Test that missing required body field raises a ValidationError."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "type": "mo_text",
        "received_at": "2024-06-06T09:22:14.304Z",
    }
    with pytest.raises(ValidationError) as exc_info:
        MOTextMessage(**data)

    assert "body" in str(exc_info.value)


def test_mo_text_message_expects_validation_error_for_missing_id():
    """Test that missing required id field raises a ValidationError."""
    data = {
        "from": "+46701234567",
        "to": "+46709876543",
        "body": "Hello world",
        "type": "mo_text",
        "received_at": "2024-06-06T09:22:14.304Z",
    }
    with pytest.raises(ValidationError) as exc_info:
        MOTextMessage(**data)

    assert "id" in str(exc_info.value)
