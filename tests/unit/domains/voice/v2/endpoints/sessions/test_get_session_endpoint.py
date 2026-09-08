from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.sessions_endpoints import (
    GetSessionEndpoint,
)
from sinch.domains.voice.models.v2.sessions.internal.request.session_id_request import (
    SessionIdRequest,
)
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.shared.money import Money
from sinch.domains.voice.models.v2.shared.phone import Phone, PhoneDetails


@pytest.fixture
def request_data():
    return SessionIdRequest(session_id="01BX5ZZKBKACTAV9WEVGEMMVRB")


@pytest.fixture
def endpoint(request_data):
    return GetSessionEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "sessionId": "01BX5ZZKBKACTAV9WEVGEMMVRB",
            "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
            "state": "COMPLETED",
            "createTime": "2025-02-10T09:00:00Z",
            "endTime": "2025-02-10T09:00:47Z",
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
                    "endTime": "2025-02-10T09:00:47Z",
                    "from": {
                        "type": "PHONE",
                        "phone": {"number": "+15551234567"},
                    },
                    "to": {
                        "type": "PHONE",
                        "phone": {"number": "+15559876543"},
                    },
                    "callRate": {"currencyCode": "USD", "amount": "0.0123"},
                    "callResourceUrl": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
                }
            ],
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
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/sessions/01BX5ZZKBKACTAV9WEVGEMMVRB",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly, including the session_id path param."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/sessions/01BX5ZZKBKACTAV9WEVGEMMVRB"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a GET endpoint with only a path param produces no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a SessionResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, SessionResponse)
    assert parsed_response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert (
        parsed_response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    )
    assert (
        parsed_response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    )
    assert parsed_response.state == "COMPLETED"
    assert parsed_response.create_time == datetime(
        2025, 2, 10, 9, 0, 0, tzinfo=timezone.utc
    )
    assert parsed_response.end_time == datetime(
        2025, 2, 10, 9, 0, 47, tzinfo=timezone.utc
    )
    assert len(parsed_response.calls) == 1
    expected_call = Call(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        direction="OUTBOUND",
        origination_type="SERVER",
        call_type="PHONE",
        call_result="COMPLETED",
        call_reason="CALLEE_HANGUP",
        start_time="2025-02-10T09:00:00Z",
        end_time="2025-02-10T09:00:47Z",
        from_=Phone(type="PHONE", phone=PhoneDetails(number="+15551234567")),
        to=Phone(type="PHONE", phone=PhoneDetails(number="+15559876543")),
        call_rate=Money(currency_code="USD", amount="0.0123"),
        call_resource_url=(
            "https://voice.api.sinch.com/v2/projects/"
            "5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/"
            "01ARZ3NDEKTSV4RRFFQ69G5FAA"
        ),
    )
    assert parsed_response.calls[0] == expected_call


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
