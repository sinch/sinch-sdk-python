from datetime import datetime, timezone
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal.inbounds_endpoints import GetInboundEndpoint
from sinch.domains.sms.models.v1.internal.inbound_id_request import InboundIdRequest
from sinch.domains.sms.models.v1.shared import MOBinaryMessage, MOTextMessage


@pytest.fixture
def request_data():
    return InboundIdRequest(inbound_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_mo_text_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "from": "+46701234567",
            "to": "+46709876543",
            "body": "Test inbound message",
            "type": "mo_text",
            "received_at": "2024-06-06T09:22:14.304Z",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetInboundEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/inbounds/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_expects_mo_text_message(endpoint, mock_mo_text_response):
    """Test that the response is correctly parsed as MOTextMessage."""
    parsed = endpoint.handle_response(mock_mo_text_response)

    assert isinstance(parsed, MOTextMessage)
    assert parsed.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed.from_ == "+46701234567"
    assert parsed.to == "+46709876543"
    assert parsed.body == "Test inbound message"
    assert parsed.type == "mo_text"
    assert parsed.received_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)


def test_handle_response_expects_mo_binary_message(request_data):
    """Test that the response is correctly parsed as MOBinaryMessage."""
    mock_binary_response = HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "from": "+46701234567",
            "to": "+46709876543",
            "body": "SGVsbG8gV29ybGQ=",
            "udh": "050003010201",
            "type": "mo_binary",
            "received_at": "2024-06-06T09:22:14.304Z",
        },
        headers={"Content-Type": "application/json"},
    )
    endpoint = GetInboundEndpoint("test_project_id", request_data)
    parsed = endpoint.handle_response(mock_binary_response)

    assert isinstance(parsed, MOBinaryMessage)
    assert parsed.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed.body == "SGVsbG8gV29ybGQ="
    assert parsed.udh == "050003010201"
    assert parsed.type == "mo_binary"


def test_handle_response_expects_sms_exception_on_error(endpoint):
    """Test that SmsException is raised when server returns an error."""
    error_response = HTTPResponse(status_code=404, body=1, headers={})

    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 404
