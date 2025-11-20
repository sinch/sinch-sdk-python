import pytest
from pydantic import ValidationError
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateTextRequestWithBatchId,
)


@pytest.fixture
def sample_update_text_request_data():
    return {
        "batch_id": "01FC77732YYYYY220A9QNW2RSQ",
        "body": "Updated message content here",
        "from_": "+46702222222",
    }


def test_update_text_request_expects_valid_inputs_and_all_fields(
    sample_update_text_request_data,
):
    """Test UpdateTextRequestWithBatchId with valid inputs and all optional fields."""
    request = UpdateTextRequestWithBatchId(**sample_update_text_request_data)
    assert request.batch_id == sample_update_text_request_data["batch_id"]
    assert request.body == sample_update_text_request_data["body"]
    assert request.from_ == sample_update_text_request_data["from_"]
    assert request.type == "mt_text"

    send_at = datetime(2025, 2, 15, 14, 30, 0, tzinfo=timezone.utc)
    expire_at = datetime(2025, 2, 18, 14, 30, 0, tzinfo=timezone.utc)

    request = UpdateTextRequestWithBatchId(
        **sample_update_text_request_data,
        to_add=["+46703333333", "+46704444444"],
        to_remove=["+46705555555"],
        delivery_report="summary",
        send_at=send_at,
        expire_at=expire_at,
        callback_url="https://capybara.com/webhook",
        client_reference="update-ref-123",
        feedback_enabled=True,
        flash_message=True,
        max_number_of_message_parts=5,
        truncate_concat=False,
        from_ton=2,
        from_npi=3,
        parameters={
            "code": {"+46703333333": "ABC123", "default": "XYZ789"},
        },
    )

    assert request.batch_id == sample_update_text_request_data["batch_id"]
    assert request.to_add == ["+46703333333", "+46704444444"]
    assert request.to_remove == ["+46705555555"]
    assert request.delivery_report == "summary"
    assert request.send_at == send_at
    assert request.expire_at == expire_at
    assert request.callback_url == "https://capybara.com/webhook"
    assert request.client_reference == "update-ref-123"
    assert request.feedback_enabled is True
    assert request.flash_message is True
    assert request.max_number_of_message_parts == 5
    assert request.truncate_concat is False
    assert request.from_ton == 2
    assert request.from_npi == 3
    assert request.parameters == {
        "code": {"+46703333333": "ABC123", "default": "XYZ789"},
    }


@pytest.mark.parametrize(
    "to_add_value",
    ["+46701234567", [123, 456], ["+46701234567", None]],
)
def test_update_text_request_expects_to_add_must_be_list_of_strings(
    sample_update_text_request_data, to_add_value
):
    """Test that to_add must be a list of strings."""
    with pytest.raises(ValidationError):
        UpdateTextRequestWithBatchId(
            **sample_update_text_request_data, to_add=to_add_value
        )


def test_update_text_request_expects_datetime_parsing(
    sample_update_text_request_data,
):
    """Test datetime parsing for send_at and expire_at."""
    send_at_str = "2025-03-20T10:15:30.123Z"
    expire_at_str = "2025-03-23T10:15:30.123Z"

    request = UpdateTextRequestWithBatchId(
        **sample_update_text_request_data,
        send_at=send_at_str,
        expire_at=expire_at_str,
    )

    assert isinstance(request.send_at, datetime)
    assert isinstance(request.expire_at, datetime)


def test_update_text_request_expects_minimal_input(
    sample_update_text_request_data,
):
    """Test UpdateTextRequestWithBatchId with only required fields."""
    request = UpdateTextRequestWithBatchId(
        batch_id=sample_update_text_request_data["batch_id"]
    )
    assert request.batch_id == sample_update_text_request_data["batch_id"]
    assert request.body is None
    assert request.from_ is None
    assert request.type == "mt_text"
    assert request.feedback_enabled is None
    assert request.flash_message is None
