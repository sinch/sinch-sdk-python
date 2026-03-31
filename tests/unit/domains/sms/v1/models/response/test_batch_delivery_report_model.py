import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.response.batch_delivery_report import (
    BatchDeliveryReport,
)


@pytest.fixture
def sample_message_delivery_status():
    """
    Sample MessageDeliveryStatus for testing.
    """
    return {
        "code": 401,
        "count": 1,
        "recipients": ["+1234567890"],
        "status": "Dispatched",
    }


@pytest.fixture
def sample_batch_delivery_report_data(sample_message_delivery_status):
    """
    Sample BatchDeliveryReport data for testing.
    """
    return {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "client_reference": "my_client_reference",
        "statuses": [sample_message_delivery_status],
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }


def test_batch_delivery_report_expects_valid_input(
    sample_batch_delivery_report_data,
):
    """
    Test that the model correctly parses valid input.
    """
    report = BatchDeliveryReport(**sample_batch_delivery_report_data)

    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.client_reference == "my_client_reference"
    assert report.total_message_count == 1
    assert report.type == "delivery_report_sms"
    assert len(report.statuses) == 1

    status = report.statuses[0]
    assert status.code == 401
    assert status.count == 1
    assert status.recipients == ["+1234567890"]
    assert status.status == "Dispatched"


def test_batch_delivery_report_expects_without_client_reference():
    """
    Test that the model works without optional client_reference.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [
            {
                "code": 401,
                "count": 1,
                "recipients": ["+44231235674"],
                "status": "Dispatched",
            }
        ],
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }

    report = BatchDeliveryReport(**data)

    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.client_reference is None
    assert report.total_message_count == 1
    assert report.type == "delivery_report_sms"


def test_batch_delivery_report_expects_with_multiple_statuses():
    """
    Test that the model works with multiple statuses.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [
            {
                "code": 401,
                "count": 1,
                "recipients": ["+44231235674"],
                "status": "Dispatched",
            },
            {
                "code": 0,
                "count": 1,
                "recipients": ["+44231235675"],
                "status": "Delivered",
            },
        ],
        "total_message_count": 2,
        "type": "delivery_report_sms",
    }

    report = BatchDeliveryReport(**data)

    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.total_message_count == 2
    assert len(report.statuses) == 2

    # Check first status
    assert report.statuses[0].code == 401
    assert report.statuses[0].status == "Dispatched"

    # Check second status
    assert report.statuses[1].code == 0
    assert report.statuses[1].status == "Delivered"


def test_batch_delivery_report_expects_no_recipients():
    """
    Test that the model works when recipients are not provided.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [{"code": 401, "count": 1, "status": "Dispatched"}],
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }

    report = BatchDeliveryReport(**data)

    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.total_message_count == 1
    assert len(report.statuses) == 1

    status = report.statuses[0]
    assert status.code == 401
    assert status.count == 1
    assert status.recipients is None
    assert status.status == "Dispatched"


def test_batch_delivery_report_expects_validation_error_for_missing_batch_id():
    """
    Test that missing required batch_id field raises a ValidationError.
    """
    data = {
        "statuses": [{"code": 401, "count": 1, "status": "Dispatched"}],
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        BatchDeliveryReport(**data)

    assert "batch_id" in str(exc_info.value)


def test_batch_delivery_report_expects_validation_error_for_missing_statuses():
    """
    Test that missing required statuses field raises a ValidationError.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        BatchDeliveryReport(**data)

    assert "statuses" in str(exc_info.value)


def test_batch_delivery_report_expects_validation_error_for_missing_total_message_count():
    """
    Test that missing required total_message_count field raises a ValidationError.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [{"code": 401, "count": 1, "status": "Dispatched"}],
        "type": "delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        BatchDeliveryReport(**data)

    assert "total_message_count" in str(exc_info.value)


def test_batch_delivery_report_expects_validation_error_for_missing_type():
    """
    Test that missing required type field raises a ValidationError.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [{"code": 401, "count": 1, "status": "Dispatched"}],
        "total_message_count": 1,
    }

    with pytest.raises(ValidationError) as exc_info:
        BatchDeliveryReport(**data)

    assert "type" in str(exc_info.value)


def test_batch_delivery_report_expects_empty_statuses():
    """
    Test that empty statuses list is allowed.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "statuses": [],
        "total_message_count": 1,
        "type": "delivery_report_sms",
    }

    report = BatchDeliveryReport(**data)
    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.statuses == []
    assert report.total_message_count == 1
    assert report.type == "delivery_report_sms"
