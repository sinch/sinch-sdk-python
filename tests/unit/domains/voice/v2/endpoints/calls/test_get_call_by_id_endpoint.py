import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    GetCallByIdEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.call_id_request import (
    CallIdRequest,
)
from sinch.domains.voice.models.v2.shared.call import Call


@pytest.fixture
def request_data():
    return CallIdRequest(call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA")


@pytest.fixture
def endpoint(request_data):
    return GetCallByIdEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "callId": "01ARZ3NDEKTSV4RRFFQ69G5FAA",
            "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
            "sessionId": "01BX5ZZKBKACTAV9WEVGEMMVRB",
            "callName": "origin",
            "direction": "OUTBOUND",
            "originationType": "SERVER",
            "callType": "PHONE",
            "callResult": "COMPLETED",
            "callReason": "CALLEE_HANGUP",
            "startTime": "2025-02-10T09:00:00Z",
            "answerTime": "2025-02-10T09:00:05Z",
            "endTime": "2025-02-10T09:00:47Z",
            "callDurationSeconds": 42,
            "from": {"type": "PHONE", "phone": {"number": "+15551234567"}},
            "to": {"type": "PHONE", "phone": {"number": "+15559876543"}},
            "callRate": {"currencyCode": "USD", "amount": "0.0123"},
            "callResourceUrl": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "type": "https://api.sinch.com/docs/errors/not-found",
            "title": "Not Found",
            "detail": "The requested resource was not found.",
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly, including the call_id path param."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a GET endpoint with only a path param produces no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a Call correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, Call)
    assert parsed_response.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert parsed_response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert parsed_response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert parsed_response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert parsed_response.call_result == "COMPLETED"


def test_handle_response_expects_voice_exception_on_error(
    endpoint, mock_error_response
):
    """Test that VoiceException is raised when the server returns an error."""
    with pytest.raises(VoiceException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == (
        "Not Found: The requested resource was not found."
    )
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
