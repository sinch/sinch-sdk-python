import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    PatchCallBySessionAndNameEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_session_and_name_request import (
    PatchCallBySessionAndNameRequest,
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
    return PatchCallBySessionAndNameRequest(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=commands,
        idempotency_key="my-custom-key",
    )


@pytest.fixture
def endpoint(request_data):
    return PatchCallBySessionAndNameEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=202,
        body={},
        headers={},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "type": "https://api.sinch.com/docs/errors/not-found",
            "title": "Not Found",
            "detail": "The requested resource was not found.",
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/sessions/01BX5ZZKBKACTAV9WEVGEMMVRB/calls/origin",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly, including the session_id and call_name path params."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/sessions/01BX5ZZKBKACTAV9WEVGEMMVRB/calls/origin"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that commands serialize correctly to the request body, applying aliases."""
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


def test_request_body_expects_path_params_and_headers_excluded(endpoint):
    """Test that path params and headers never leak into the body."""
    body = json.loads(endpoint.request_body())

    assert "project_id" not in body
    assert "session_id" not in body
    assert "sessionId" not in body
    assert "call_name" not in body
    assert "callName" not in body
    assert "Idempotency-Key" not in body


def test_build_headers_expects_correct_serialization(commands):
    """Test that headers defined in the endpoint are correctly built."""
    endpoint = PatchCallBySessionAndNameEndpoint(
        "test_project_id",
        PatchCallBySessionAndNameRequest(
            session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
            call_name="origin",
            commands=commands,
            idempotency_key="my-custom-key",
        ),
    )

    assert endpoint.build_headers() == {"Idempotency-Key": "my-custom-key"}


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and returns none correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert parsed_response is None


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
