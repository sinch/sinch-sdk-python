import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import (
    GetRecipientDeliveryReportEndpoint,
)
from sinch.domains.sms.models.v1.internal import (
    GetRecipientDeliveryReportRequest,
)
from sinch.domains.sms.models.v1.response import RecipientDeliveryReport


@pytest.fixture
def request_data():
    return GetRecipientDeliveryReportRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ", recipient_msisdn="+1234567890"
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
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
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetRecipientDeliveryReportEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://mock-sms-api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ/delivery_report/+1234567890"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)
    assert isinstance(parsed_response, RecipientDeliveryReport)
    assert parsed_response.applied_originator == "+1234567890"
    assert parsed_response.at == (
        datetime(2025, 1, 15, 10, 30, 45, 123000, tzinfo=timezone.utc)
    )
    assert parsed_response.batch_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.client_reference == "test_client_ref"
    assert parsed_response.code == 400
    assert parsed_response.encoding == "GSM7"
    assert parsed_response.number_of_message_parts == 1
    assert parsed_response.operator == "35000"
    assert parsed_response.operator_status_at == (
        datetime(2025, 1, 15, 10, 30, 50, 456000, tzinfo=timezone.utc)
    )
    assert parsed_response.recipient == "+1234567890"
    assert parsed_response.status == "DELIVERED"
    assert parsed_response.type == "recipient_delivery_report_sms"
