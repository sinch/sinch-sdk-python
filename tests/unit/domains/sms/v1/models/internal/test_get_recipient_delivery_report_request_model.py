import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import GetRecipientDeliveryReportRequest


@pytest.mark.parametrize(
    "batch_id, recipient_msisdn",
    [
        ("01FC66621XXXXX119Z8PMV1QPQ", "+44231235674"),
        ("batch123", "+15551234567"),
        ("test-batch-456", "+1234567890"),
    ]
)
def test_get_recipient_delivery_report_request_expects_valid_inputs(batch_id, recipient_msisdn):
    """
    Test that the model correctly parses valid inputs.
    """
    data = {
        "batch_id": batch_id,
        "recipient_msisdn": recipient_msisdn
    }

    request = GetRecipientDeliveryReportRequest(**data)

    assert request.batch_id == batch_id
    assert request.recipient_msisdn == recipient_msisdn


def test_get_recipient_delivery_report_request_expects_validation_error_for_missing_batch_id():
    """
    Test that missing batch_id raises a ValidationError.
    """
    data = {
        "recipient_msisdn": "+44231235674"
    }
    
    with pytest.raises(ValidationError) as exc_info:
            GetRecipientDeliveryReportRequest(**data)
    
    assert "batch_id" in str(exc_info.value)


def test_get_recipient_delivery_report_request_expects_validation_error_for_missing_recipient_msisdn():
    """
    Test that missing recipient_msisdn raises a ValidationError.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ"
    }
    
    with pytest.raises(ValidationError) as exc_info:
            GetRecipientDeliveryReportRequest(**data)
    
    assert "recipient_msisdn" in str(exc_info.value)


def test_get_recipient_delivery_report_request_with_additional_kwargs():
    """
    Test that additional kwargs are handled properly.
    """
    data = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "recipient_msisdn": "+44231235674",
        "extra_field": "extra_value"
    }

    request = GetRecipientDeliveryReportRequest(**data)

    assert request.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert request.recipient_msisdn == "+44231235674"
