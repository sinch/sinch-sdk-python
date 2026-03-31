import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.response.recipient_delivery_report import (
    RecipientDeliveryReport,
)
from tests.conftest import parse_iso_datetime


@pytest.fixture
def sample_recipient_delivery_report_data():
    """
    Sample data for RecipientDeliveryReport testing.
    """
    return {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "recipient_delivery_report_sms",
    }


@pytest.mark.parametrize(
    "status, code, report_type",
    [
        ("Delivered", 401, "recipient_delivery_report_sms"),
        ("Failed", 402, "recipient_delivery_report_sms"),
        ("Queued", 400, "recipient_delivery_report_mms"),
        ("Dispatched", 401, "recipient_delivery_report_mms"),
    ],
)
def test_recipient_delivery_report_expects_valid_inputs(
    status, code, report_type
):
    """
    Test that the model correctly parses valid inputs with different statuses and codes.
    """
    data = {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": code,
        "recipient": "+44231235674",
        "status": status,
        "type": report_type,
    }

    report = RecipientDeliveryReport(**data)

    assert report.at == parse_iso_datetime("2022-08-30T08:16:08.930Z")
    assert report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert report.code == code
    assert report.recipient == "+44231235674"
    assert report.status == status
    assert report.type == report_type


def test_recipient_delivery_report_expects_with_optional_fields(
    sample_recipient_delivery_report_data,
):
    """
    Test that the model works with all optional fields provided.
    """
    data = sample_recipient_delivery_report_data.copy()
    data.update(
        {
            "applied_originator": "My Originator",
            "client_reference": "my_client_reference",
            "encoding": "GSM",
            "number_of_message_parts": 1,
            "operator": "35000",
            "operator_status_at": parse_iso_datetime("2019-08-24T14:15:22Z"),
        }
    )

    report = RecipientDeliveryReport(**data)

    assert report.applied_originator == "My Originator"
    assert report.client_reference == "my_client_reference"
    assert report.encoding == "GSM"
    assert report.number_of_message_parts == 1
    assert report.operator == "35000"
    assert report.operator_status_at == parse_iso_datetime(
        "2019-08-24T14:15:22Z"
    )


def test_recipient_delivery_report_expects_without_optional_fields(
    sample_recipient_delivery_report_data,
):
    """
    Test that the model works without optional fields.
    """
    report = RecipientDeliveryReport(**sample_recipient_delivery_report_data)

    assert report.applied_originator is None
    assert report.client_reference is None
    assert report.encoding is None
    assert report.number_of_message_parts is None
    assert report.operator is None
    assert report.operator_status_at is None


def test_recipient_delivery_report_expects_validation_error_for_missing_at():
    """
    Test that missing 'at' field raises a ValidationError.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "recipient_delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        RecipientDeliveryReport(**data)

    assert "at" in str(exc_info.value)


def test_recipient_delivery_report_expects_validation_error_for_missing_batch_id():
    """
    Test that missing 'batch_id' field raises a ValidationError.
    """
    data = {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "recipient_delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        RecipientDeliveryReport(**data)

    assert "batch_id" in str(exc_info.value)


def test_recipient_delivery_report_expects_invalid_datetime_format():
    """
    Test that invalid datetime format raises a ValidationError.
    """
    data = {
        "at": "invalid-datetime",
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "recipient_delivery_report_sms",
    }

    with pytest.raises(ValidationError) as exc_info:
        RecipientDeliveryReport(**data)

    assert "at" in str(exc_info.value)


def test_recipient_delivery_report_expects_custom_encoding():
    """
    Test that the model accepts custom encoding values due to Union + StrictStr.
    """
    data = {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "recipient_delivery_report_sms",
        "encoding": "CUSTOM_ENCODING",
    }

    report = RecipientDeliveryReport(**data)
    assert report.encoding == "CUSTOM_ENCODING"


def test_recipient_delivery_report_expects_custom_status():
    """
    Test that the model accepts custom status values due to Union + StrictStr.
    """
    data = {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "CUSTOM_STATUS",
        "type": "recipient_delivery_report_sms",
    }

    report = RecipientDeliveryReport(**data)
    assert report.status == "CUSTOM_STATUS"


def test_recipient_delivery_report_expects_custom_type():
    """
    Test that the model accepts custom type values due to Union + StrictStr.
    """
    data = {
        "at": parse_iso_datetime("2022-08-30T08:16:08.930Z"),
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "code": 401,
        "recipient": "+44231235674",
        "status": "Dispatched",
        "type": "custom_delivery_report_type",
    }

    report = RecipientDeliveryReport(**data)
    assert report.type == "custom_delivery_report_type"
