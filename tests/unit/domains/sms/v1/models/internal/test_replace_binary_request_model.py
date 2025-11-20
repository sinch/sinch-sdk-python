import pytest
from pydantic import ValidationError
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceBinaryRequest,
)


@pytest.fixture
def sample_replace_binary_request_data():
    return {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": ["+46701234567", "+46709876543"],
        "from_": "+46701111111",
        "body": "SGVsbG8gV29ybGQh",
        "udh": "06050423F423F4",
    }


def test_replace_binary_request_expects_valid_inputs_and_all_fields(
    sample_replace_binary_request_data,
):
    """Test ReplaceBinaryRequest with valid inputs and all optional fields."""
    request = ReplaceBinaryRequest(**sample_replace_binary_request_data)
    assert request.batch_id == sample_replace_binary_request_data["batch_id"]
    assert request.to == sample_replace_binary_request_data["to"]
    assert request.from_ == sample_replace_binary_request_data["from_"]
    assert request.body == sample_replace_binary_request_data["body"]
    assert request.udh == sample_replace_binary_request_data["udh"]
    assert request.type == "mt_binary"
    assert request.delivery_report is None
    assert request.feedback_enabled is None

    send_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    expire_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

    request = ReplaceBinaryRequest(
        **sample_replace_binary_request_data,
        delivery_report="summary",
        send_at=send_at,
        expire_at=expire_at,
        callback_url="https://capybara.com/callback",
        client_reference="test-ref",
        feedback_enabled=True,
        from_ton=1,
        from_npi=1,
    )

    assert request.delivery_report == "summary"
    assert request.send_at == send_at
    assert request.expire_at == expire_at
    assert request.callback_url == "https://capybara.com/callback"
    assert request.client_reference == "test-ref"
    assert request.feedback_enabled is True
    assert request.from_ton == 1
    assert request.from_npi == 1


@pytest.mark.parametrize(
    "missing_field",
    ["batch_id", "to", "body", "udh"],
)
def test_replace_binary_request_expects_required_fields(
    sample_replace_binary_request_data, missing_field
):
    """Test that ReplaceBinaryRequest requires batch_id, to, body, and udh fields."""
    data = sample_replace_binary_request_data.copy()
    data.pop(missing_field)
    with pytest.raises(ValidationError) as exc_info:
        ReplaceBinaryRequest(**data)
    assert missing_field in str(exc_info.value)
