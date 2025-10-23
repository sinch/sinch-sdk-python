from datetime import datetime, timezone
import pytest
from sinch.domains.sms.models.v1.internal import ListDeliveryReportsResponse


@pytest.fixture
def test_data():
    return {
        "count": 2,
        "page": 0,
        "page_size": 2,
        "delivery_reports": [
            {
                "at": "2025-01-19T16:45:31.935Z",
                "batch_id": "01K7YNS82JMYGAKAATHFP0QTB5",
                "code": 401,
                "operator_status_at": "2025-01-19T16:45:00Z",
                "recipient": "34683607594",
                "status": "Delivered",
                "type": "recipient_delivery_report_sms",
            },
            {
                "at": "2025-01-19T16:40:26.855Z",
                "batch_id": "01K7YNFY30DS2KKVQZVBFANHMR",
                "code": 402,
                "operator_status_at": "2025-01-19T16:40:00Z",
                "recipient": "34683607595",
                "status": "Dispatched",
                "type": "recipient_delivery_report_sms",
            },
        ],
    }


def assert_delivery_report_fields(delivery_report, expected_batch_id, expected_recipient, expected_code, expected_status):
    """Helper function to assert delivery report fields."""
    assert delivery_report.batch_id == expected_batch_id
    assert delivery_report.recipient == expected_recipient
    assert delivery_report.code == expected_code
    assert delivery_report.status == expected_status
    assert delivery_report.type == "recipient_delivery_report_sms"


def test_list_delivery_reports_response_empty_content_expects_empty_list():
    """Test that empty delivery reports list returns empty content."""
    model = ListDeliveryReportsResponse(count=0, page=0, page_size=30, delivery_reports=None)
    assert model.count == 0
    assert model.page == 0
    assert model.page_size == 30
    assert model.content == []


def test_list_delivery_reports_response_expects_correct_mapping(test_data):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    response = ListDeliveryReportsResponse(**test_data)
    assert hasattr(response, "content")
    assert response.content == response.delivery_reports
    
    # Test top-level fields
    assert response.count == 2
    assert response.page == 0
    assert response.page_size == 2
    
    # Test content property
    content = response.content
    assert isinstance(content, list)
    assert len(content) == 2
    
    # Test first delivery report
    first_report = content[0]
    expected_first_at = datetime(2025, 1, 19, 16, 45, 31, 935000, tzinfo=timezone.utc)
    expected_first_operator_at = datetime(2025, 1, 19, 16, 45, 0, tzinfo=timezone.utc)
    assert first_report.at == expected_first_at
    assert first_report.operator_status_at == expected_first_operator_at
    assert_delivery_report_fields(
        first_report, 
        "01K7YNS82JMYGAKAATHFP0QTB5", 
        "34683607594", 
        401, 
        "Delivered"
    )
    
    # Test second delivery report
    second_report = content[1]
    expected_second_at = datetime(2025, 1, 19, 16, 40, 26, 855000, tzinfo=timezone.utc)
    expected_second_operator_at = datetime(2025, 1, 19, 16, 40, 0, tzinfo=timezone.utc)
    assert second_report.at == expected_second_at
    assert second_report.operator_status_at == expected_second_operator_at
    assert_delivery_report_fields(
        second_report, 
        "01K7YNFY30DS2KKVQZVBFANHMR", 
        "34683607595", 
        402, 
        "Dispatched"
    )


