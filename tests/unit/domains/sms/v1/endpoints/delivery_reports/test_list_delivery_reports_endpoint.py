import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import ListDeliveryReportsEndpoint
from sinch.domains.sms.models.v1.internal import ListDeliveryReportsRequest
from sinch.domains.sms.models.v1.response import RecipientDeliveryReport


@pytest.fixture
def request_data():
    return ListDeliveryReportsRequest(
        page=0,
        page_size=10,
        start_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 6, 30, tzinfo=timezone.utc),
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "count": 2,
            "page": 0,
            "page_size": 10,
            "delivery_reports": [
                {
                    "applied_originator": "+1234567890",
                    "at": "2025-01-15T10:30:45.123Z",
                    "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
                    "client_reference": "test_client_ref",
                    "code": 400,
                    "encoding": "GSM7",
                    "number_of_message_parts": 1,
                    "operator": "35000",
                    "operator_status_at": "2025-01-15T10:30:50.456Z",
                    "recipient": "+1234567890",
                    "status": "DELIVERED",
                    "type": "recipient_delivery_report_sms",
                },
                {
                    "applied_originator": "+1234567890",
                    "at": "2025-01-16T10:30:45.123Z",
                    "batch_id": "01W4FFL35P4NC4K35SMSBATCH1",
                    "client_reference": "test_client_ref",
                    "code": 401,
                    "encoding": "GSM7",
                    "number_of_message_parts": 1,
                    "operator": "35000",
                    "operator_status_at": "2025-01-16T10:30:50.456Z",
                    "recipient": "+0987654321",
                    "status": "FAILED",
                    "type": "recipient_delivery_report_sms",
                },
            ],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListDeliveryReportsEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/delivery_reports"
    )


def test_build_query_params_expects_all_params():
    """Test that multiple status and code values are converted to comma-separated strings"""
    request_data = ListDeliveryReportsRequest(
        page=1,
        page_size=20,
        start_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 6, 30, tzinfo=timezone.utc),
        status=["DELIVERED", "FAILED", "QUEUED"],
        code=[400, 401, 402],
        client_reference="test_client_ref",
    )
    endpoint = ListDeliveryReportsEndpoint("test_project_id", request_data)
    query_params = endpoint.build_query_params()
    assert query_params["page"] == 1
    assert query_params["page_size"] == 20
    assert query_params["start_date"] == "2024-06-01T00:00:00Z"
    assert query_params["end_date"] == "2024-06-30T00:00:00Z"
    assert query_params["status"] == "DELIVERED,FAILED,QUEUED"
    assert query_params["code"] == "400,401,402"
    assert query_params["client_reference"] == "test_client_ref"


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert parsed_response.count == 2
    assert parsed_response.page == 0
    assert parsed_response.page_size == 10
    assert parsed_response.content == parsed_response.delivery_reports
    assert len(parsed_response.delivery_reports) == 2

    first_report = parsed_response.delivery_reports[0]
    assert isinstance(first_report, RecipientDeliveryReport)
    assert first_report.applied_originator == "+1234567890"
    assert first_report.at == (
        datetime(2025, 1, 15, 10, 30, 45, 123000, tzinfo=timezone.utc)
    )
    assert first_report.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert first_report.client_reference == "test_client_ref"
    assert first_report.code == 400
    assert first_report.status == "DELIVERED"
    assert first_report.recipient == "+1234567890"

    second_report = parsed_response.delivery_reports[1]
    assert isinstance(second_report, RecipientDeliveryReport)
    assert second_report.batch_id == "01W4FFL35P4NC4K35SMSBATCH1"
    assert second_report.code == 401
    assert second_report.status == "FAILED"
    assert second_report.recipient == "+0987654321"
