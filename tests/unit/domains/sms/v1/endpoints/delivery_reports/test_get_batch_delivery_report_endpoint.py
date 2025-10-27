import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import GetBatchDeliveryReportEndpoint
from sinch.domains.sms.models.v1.internal import GetBatchDeliveryReportRequest
from sinch.domains.sms.models.v1.response import BatchDeliveryReport
from sinch.domains.sms.models.v1.shared import MessageDeliveryStatus


@pytest.fixture
def request_data():
    return GetBatchDeliveryReportRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        type="summary",
        status=["DELIVERED"],
        code=[400],
        client_reference="test_client_ref",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
            "client_reference": "test_client_ref",
            "statuses": [
                {
                    "code": 400,
                    "count": 5,
                    "recipients": ["+1234567890", "+0987654321"],
                    "status": "DELIVERED",
                },
                {
                    "code": 401,
                    "count": 2,
                    "recipients": ["+5555555555"],
                    "status": "FAILED",
                },
            ],
            "total_message_count": 7,
            "type": "summary",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetBatchDeliveryReportEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://mock-sms-api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ/delivery_report"
    )


def test_build_query_params(endpoint):
    query_params = endpoint.build_query_params()
    expected_params = {
        "batch_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "type": "summary",
        "status": "DELIVERED",
        "code": "400",
        "client_reference": "test_client_ref",
    }
    assert query_params == expected_params


def test_build_query_params_with_multiple_status_and_code():
    """Test that multiple status and code values are converted to comma-separated strings"""
    request_data = GetBatchDeliveryReportRequest(
        batch_id="01W4FFL35P4NC4K35SMSBATCH1",
        status=["DELIVERED", "FAILED", "QUEUED"],
        code=[400, 401, 402],
    )
    endpoint = GetBatchDeliveryReportEndpoint("test_project_id", request_data)
    query_params = endpoint.build_query_params()
    expected_params = {
        "batch_id": "01W4FFL35P4NC4K35SMSBATCH1",
        "status": "DELIVERED,FAILED,QUEUED",
        "code": "400,401,402",
    }
    assert query_params == expected_params


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, BatchDeliveryReport)
    assert parsed_response.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.client_reference == "test_client_ref"
    assert parsed_response.total_message_count == 7
    assert parsed_response.type == "summary"

    assert len(parsed_response.statuses) == 2

    first_status = parsed_response.statuses[0]
    assert isinstance(first_status, MessageDeliveryStatus)
    assert first_status.code == 400
    assert first_status.count == 5
    assert first_status.status == "DELIVERED"
    assert first_status.recipients == ["+1234567890", "+0987654321"]

    second_status = parsed_response.statuses[1]
    assert isinstance(second_status, MessageDeliveryStatus)
    assert second_status.code == 401
    assert second_status.count == 2
    assert second_status.status == "FAILED"
    assert second_status.recipients == ["+5555555555"]
