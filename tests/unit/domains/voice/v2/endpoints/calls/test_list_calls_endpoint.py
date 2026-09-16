from datetime import datetime

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    ListCallsEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.list_calls_response import (
    ListCallsResponse,
)
from sinch.domains.voice.models.v2.calls.internal.request.list_calls_request import (
    ListCallsRequest,
)


@pytest.fixture
def request_data():
    return ListCallsRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        from_="+15551234567",
        to="+15551234568",
        call_type="PHONE",
        start_time=datetime(2025, 2, 1, 14, 0, 0),
        end_time=datetime(2025, 3, 1, 14, 0, 0),
        call_result="COMPLETED",
        call_reason="CALLEE_HANGUP",
        page_size=1,
        page=2,
    )


@pytest.fixture
def endpoint(request_data):
    return ListCallsEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "calls": [
                {
                    "callId": "01ARZ3NDEKTSV4RRFFQ69G5FAA",
                    "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
                    "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
                    "sessionId": "01BX5ZZKBKACTAV9WEVGEMMVRB",
                    "direction": "OUTBOUND",
                    "originationType": "SERVER",
                    "callType": "PHONE",
                    "callResult": "COMPLETED",
                    "callReason": "CALLEE_HANGUP",
                    "startTime": "2025-02-10T09:00:00Z",
                    "callRate": {"currencyCode": "USD", "amount": "0.0123"},
                    "callResourceUrl": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
                }
            ],
            "links": {
                "first": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1",
                "last": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=1",
                "next": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=3&pageSize=1",
                "self": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=1",
                "prev": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1",
            },
            "meta": {"totalCount": 5, "pageCount": 5},
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=400,
        body={
            "type": "https://api.sinch.com/docs/errors/bad-request",
            "title": "Bad Request",
            "detail": "The request body is invalid or malformed.",
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_voice)
        == "https://voice.api.sinch.com/v2/projects/test_project_id/calls"
    )


def test_build_query_params_expects_correct_serialization(endpoint):
    """Test that all query fields serialize correctly, applying aliases."""
    assert endpoint.build_query_params() == {
        "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
        "from": "+15551234567",
        "to": "+15551234568",
        "callType": "PHONE",
        "startTime": "2025-02-01T14:00:00",
        "endTime": "2025-03-01T14:00:00",
        "callResult": "COMPLETED",
        "callReason": "CALLEE_HANGUP",
        "pageSize": 1,
        "page": 2,
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that fields passed as None are excluded from the query params."""
    endpoint = ListCallsEndpoint("test_project_id", ListCallsRequest())

    assert endpoint.build_query_params() == {}


def test_request_body_expects_no_body(endpoint):
    """Test that the dumped body is empty since every field is a query param."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ListCallsResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListCallsResponse)
    assert len(parsed_response.calls) == 1
    assert parsed_response.calls[0].call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert parsed_response.content == parsed_response.calls
    assert parsed_response.links.next == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=3&pageSize=1"
    )
    assert parsed_response.links.prev == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1"
    )
    assert parsed_response.links.self_ == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=1"
    )
    assert parsed_response.links.first == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=1"
    )
    assert parsed_response.links.last == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=1"
    )
    assert parsed_response.meta.total_count == 5
    assert parsed_response.meta.page_count == 5


def test_handle_response_expects_voice_exception_on_error(
    endpoint, mock_error_response
):
    """Test that VoiceException is raised when the server returns an error."""
    with pytest.raises(VoiceException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == (
        "Bad Request: The request body is invalid or malformed."
    )
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
