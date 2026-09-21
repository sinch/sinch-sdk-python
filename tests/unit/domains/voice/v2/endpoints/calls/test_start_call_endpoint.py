import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    StartCallEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)


@pytest.fixture
def commands():
    return [
        {
            "command": "dial",
            "call_name": "origin",
            "from_": {"type": "PHONE", "phone": {"number": "+15551234567"}},
            "to": {"type": "PHONE", "phone": {"number": "+15559876543"}},
            "dial_timeout_duration_seconds": 30,
            "max_call_duration_seconds": 3600,
            "events": {
                "on_answer": [
                    {
                        "command": "messages",
                        "messages": [
                            {
                                "type": "SAY",
                                "say": {
                                    "text": "Hello, your call is now connected.",
                                    "voice_name": "Emma",
                                },
                            }
                        ],
                    }
                ],
                "on_hangup": [{"command": "hangup"}],
            },
        }
    ]


@pytest.fixture
def request_data(commands):
    return StartCallRequest(
        commands=commands,
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        idempotency_key="my-custom-key",
    )


@pytest.fixture
def endpoint(request_data):
    return StartCallEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=201,
        body={
            "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
            "sessionId": "01BX5ZZKBKACTAV9WEVGEMMVRB",
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


def test_build_query_params_expects_service_id(endpoint):
    """Test that service_id is sent as the serviceId query param."""
    assert endpoint.build_query_params() == {
        "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade"
    }


def test_build_query_params_expects_none_field_excluded(commands):
    """Test that a service_id passed as None is excluded from the query params."""
    endpoint = StartCallEndpoint(
        "test_project_id",
        StartCallRequest(commands=commands, service_id=None),
    )

    assert endpoint.build_query_params() == {}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that all fields serialize correctly to the request body, applying aliases."""
    body = json.loads(endpoint.request_body())

    dial = body["commands"][0]
    assert dial["command"] == "dial"
    assert dial["callName"] == "origin"
    assert dial["from"] == {
        "type": "PHONE",
        "phone": {"number": "+15551234567"},
    }
    assert dial["to"] == {"type": "PHONE", "phone": {"number": "+15559876543"}}
    assert dial["dialTimeoutDurationSeconds"] == 30
    assert dial["maxCallDurationSeconds"] == 3600
    on_answer = dial["events"]["onAnswer"][0]
    assert on_answer["command"] == "messages"
    message = on_answer["messages"][0]
    assert message["type"] == "SAY"
    assert message["say"]["text"] == "Hello, your call is now connected."
    assert message["say"]["voiceName"] == "Emma"
    assert dial["events"]["onHangup"] == [{"command": "hangup"}]


def test_request_body_expects_path_query_params_and_headers_excluded(endpoint):
    """Test that path params, query params, and headers never leak into the body."""
    body = json.loads(endpoint.request_body())

    assert "project_id" not in body
    assert "service_id" not in body
    assert "serviceId" not in body
    assert "Idempotency-Key" not in body


def test_build_headers_expects_correct_serialization(commands):
    """Test that headers defined in the endpoint are correctly built."""
    endpoint = StartCallEndpoint(
        "test_project_id",
        StartCallRequest(commands=commands, idempotency_key="my-custom-key"),
    )

    assert endpoint.build_headers() == {"Idempotency-Key": "my-custom-key"}


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a StartCallResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, StartCallResponse)
    assert parsed_response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert parsed_response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert parsed_response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"


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


def test_handle_response_expects_error_type_and_instance_on_error(
    endpoint, mock_error_response
):
    """Test that VoiceException exposes the error's type and instance fields."""
    with pytest.raises(VoiceException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.error_type == (
        "https://api.sinch.com/docs/errors/bad-request"
    )
    assert exc_info.value.instance == (
        "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls"
    )
