import pytest
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateBinaryRequestWithBatchId,
)


@pytest.fixture
def sample_update_binary_request_data():
    return {
        "batch_id": "01FC88843ZZZZZ331B0ROX3STQ",
        "udh": "06050423F423F5",
        "body": "VXBkYXRlZCBiaW5hcnkgY29udGVudA==",
    }


def test_update_binary_request_expects_valid_inputs_and_all_fields(
    sample_update_binary_request_data,
):
    """Test UpdateBinaryRequestWithBatchId with valid inputs and all optional fields."""
    request = UpdateBinaryRequestWithBatchId(
        **sample_update_binary_request_data
    )
    assert request.batch_id == sample_update_binary_request_data["batch_id"]
    assert request.udh == sample_update_binary_request_data["udh"]
    assert request.body == sample_update_binary_request_data["body"]
    assert request.type == "mt_binary"

    send_at = datetime(2025, 4, 10, 16, 45, 0, tzinfo=timezone.utc)
    expire_at = datetime(2025, 4, 13, 16, 45, 0, tzinfo=timezone.utc)

    request = UpdateBinaryRequestWithBatchId(
        **sample_update_binary_request_data,
        from_="+46706666666",
        to_add=["+46707777777", "+46708888888"],
        to_remove=["+46709999999"],
        delivery_report="full",
        send_at=send_at,
        expire_at=expire_at,
        callback_url="https://capybara.com/binary-callback",
        client_reference="binary-update-456",
        feedback_enabled=True,
        from_ton=3,
        from_npi=4,
    )

    assert request.batch_id == sample_update_binary_request_data["batch_id"]
    assert request.udh == sample_update_binary_request_data["udh"]
    assert request.from_ == "+46706666666"
    assert request.to_add == ["+46707777777", "+46708888888"]
    assert request.to_remove == ["+46709999999"]
    assert request.delivery_report == "full"
    assert request.send_at == send_at
    assert request.expire_at == expire_at
    assert request.callback_url == "https://capybara.com/binary-callback"
    assert request.client_reference == "binary-update-456"
    assert request.feedback_enabled is True
    assert request.from_ton == 3
    assert request.from_npi == 4


def test_update_binary_request_expects_datetime_parsing(
    sample_update_binary_request_data,
):
    """Test datetime parsing for send_at and expire_at."""
    send_at_str = "2025-05-25T08:20:45.456Z"
    expire_at_str = "2025-05-28T08:20:45.456Z"

    request = UpdateBinaryRequestWithBatchId(
        **sample_update_binary_request_data,
        send_at=send_at_str,
        expire_at=expire_at_str,
    )

    assert isinstance(request.send_at, datetime)
    assert isinstance(request.expire_at, datetime)


def test_update_binary_request_expects_minimal_input(
    sample_update_binary_request_data,
):
    """Test UpdateBinaryRequestWithBatchId with only required fields."""
    request = UpdateBinaryRequestWithBatchId(
        batch_id=sample_update_binary_request_data["batch_id"],
        udh=sample_update_binary_request_data["udh"],
    )
    assert request.batch_id == sample_update_binary_request_data["batch_id"]
    assert request.udh == sample_update_binary_request_data["udh"]
    assert request.body is None
    assert request.type == "mt_binary"
    assert request.feedback_enabled is None
