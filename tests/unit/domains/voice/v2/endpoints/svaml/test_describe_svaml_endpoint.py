import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.svaml_endpoints import (
    DescribeSvamlEndpoint,
)
from sinch.domains.voice.models.v2.svaml.internal.request.describe_svaml_request import (
    DescribeSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)


@pytest.fixture
def request_data():
    return DescribeSvamlRequest(
        svaml={
            "commands": [
                {"command": "answer"},
                {
                    "command": "messages",
                    "messages": [
                        {
                            "type": "SAY",
                            "say": {
                                "text": "Welcome to ACME support.",
                                "voiceName": "Emma",
                            },
                        }
                    ],
                },
            ]
        }
    )


@pytest.fixture
def endpoint(request_data):
    return DescribeSvamlEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "description": "The call is answered and a TTS message is played using the voice Emma."
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
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/svaml/describe",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/svaml/describe"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that all fields serialize correctly to the request body."""
    body = json.loads(endpoint.request_body())

    assert body["svaml"]["commands"][0]["command"] == "answer"
    assert body["svaml"]["commands"][1]["command"] == "messages"
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an omitted field is absent and a provided value is present."""
    endpoint = DescribeSvamlEndpoint(
        "test_project_id",
        DescribeSvamlRequest(svaml={"commands": [{"command": "answer"}]}),
    )
    body = json.loads(endpoint.request_body())

    assert body["svaml"]["commands"][0]["command"] == "answer"


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a DescribeSvamlResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, DescribeSvamlResponse)
    assert parsed_response.description == (
        "The call is answered and a TTS message is played using the voice Emma."
    )


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
