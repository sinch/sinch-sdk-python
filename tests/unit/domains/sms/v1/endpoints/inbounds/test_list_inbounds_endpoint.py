from datetime import datetime, timezone
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal.inbounds_endpoints import ListInboundsEndpoint
from sinch.domains.sms.models.v1.internal.list_inbounds_request import ListInboundsRequest
from sinch.domains.sms.models.v1.internal.list_inbounds_response import ListInboundsResponse
from sinch.domains.sms.models.v1.shared import MOTextMessage


@pytest.fixture
def request_data():
    return ListInboundsRequest(
        page=0,
        page_size=2,
        to=["+46709876543"],
        client_reference="ref123",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "count": 1,
            "page": 0,
            "page_size": 2,
            "inbounds": [
                {
                    "id": "01FC66621XXXXX119Z8PMV1QPQ",
                    "from": "+46701234567",
                    "to": "+46709876543",
                    "body": "Test inbound message",
                    "type": "mo_text",
                    "received_at": "2024-06-06T09:22:14.304Z",
                }
            ],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListInboundsEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/inbounds"
    )


def test_build_query_params_expects_all_params(endpoint):
    query_params = endpoint.build_query_params()

    assert query_params["page"] == 0
    assert query_params["page_size"] == 2
    assert query_params["to"] == "+46709876543"
    assert query_params["client_reference"] == "ref123"


def test_build_query_params_expects_excludes_none_values():
    """Test that None values are excluded from query parameters."""
    endpoint = ListInboundsEndpoint(
        "test_project_id", ListInboundsRequest()
    )
    query_params = endpoint.build_query_params()

    assert len(query_params) == 0
    assert "page" not in query_params
    assert "page_size" not in query_params
    assert "to" not in query_params
    assert "start_date" not in query_params
    assert "end_date" not in query_params
    assert "client_reference" not in query_params


def test_build_query_params_expects_date_filters():
    """Test that date filters are included when provided."""
    request_data = ListInboundsRequest(
        start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 31, tzinfo=timezone.utc),
    )
    endpoint = ListInboundsEndpoint("test_project_id", request_data)
    query_params = endpoint.build_query_params()

    assert "start_date" in query_params
    assert "end_date" in query_params


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is handled and mapped to the appropriate fields correctly."""
    parsed = endpoint.handle_response(mock_response)

    assert isinstance(parsed, ListInboundsResponse)
    assert parsed.count == 1
    assert parsed.page == 0
    assert parsed.page_size == 2
    assert parsed.inbounds is not None
    assert len(parsed.inbounds) == 1

    first_inbound = parsed.inbounds[0]
    assert isinstance(first_inbound, MOTextMessage)
    assert first_inbound.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert first_inbound.from_ == "+46701234567"
    assert first_inbound.body == "Test inbound message"
    assert first_inbound.type == "mo_text"


def test_handle_response_expects_sms_exception_on_error(endpoint):
    """Test that SmsException is raised when server returns an error."""
    error_response = HTTPResponse(status_code=404, body=1, headers={})

    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(error_response)

    assert exc_info.value.args[0] == "Error 404"
    assert exc_info.value.http_response == error_response
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 404
