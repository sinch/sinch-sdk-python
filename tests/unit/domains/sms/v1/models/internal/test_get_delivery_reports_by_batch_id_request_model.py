import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.internal import GetDeliveryReportsByBatchIdRequest
from sinch.domains.sms.models.v1.types import DeliveryStatusType, DeliveryReceiptStatusCodeType


@pytest.mark.parametrize(
    "batch_id, report_type, status, code, expected_report_type",
    [
        ("batch123", "summary", ["Queued", "Dispatched"], [400, 401], "summary"),
        ("batch456", "full", ["Dispatched", "Delivered"], [401, 400], "full"),
        ("batch789", None, ["Failed", "Cancelled"], [402, 403], "summary"),  # Default value
    ]
)
def test_get_delivery_reports_by_batch_id_request_expects_valid_input(
    batch_id, report_type, status, code, expected_report_type
):
    """
    Test that the model correctly parses valid inputs.
    """
    data = {
        "batch_id": batch_id,
        "type": report_type,
        "status": status,
        "code": code
    }
    
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}
    
    request = GetDeliveryReportsByBatchIdRequest(**data)
    
    assert request.batch_id == batch_id
    assert request.type == expected_report_type
    assert request.status == status
    assert request.code == code


def test_get_delivery_reports_by_batch_id_request_expects_status_list():
    """
    Test that the model correctly handles status list input.
    """
    data = {
        "batch_id": "batch123",
        "status": ["QUEUED", "DELIVERED", "FAILED"]
    }
    
    request = GetDeliveryReportsByBatchIdRequest(**data)
    
    assert request.batch_id == "batch123"
    assert request.status == ["QUEUED", "DELIVERED", "FAILED"]
    assert request.type == "summary"  # Default value
    assert request.code is None


def test_get_delivery_reports_by_batch_id_request_ecpects_code_list():
    """
    Test that the model correctly handles code list input.
    """
    data = {
        "batch_id": "batch123",
        "code": [400, 401, 402]
    }
    
    request = GetDeliveryReportsByBatchIdRequest(**data)
    
    assert request.batch_id == "batch123"
    assert request.code == [400, 401, 402]
    assert request.type == "summary"  # Default value
    assert request.status is None


def test_get_delivery_reports_by_batch_id_request_expects_validation_error_for_missing_batch_id():
    """
    Test that missing required batch_id field raises a ValidationError.
    """
    data = {
        "type": "summary"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        GetDeliveryReportsByBatchIdRequest(**data)
    
    assert "batch_id" in str(exc_info.value)
