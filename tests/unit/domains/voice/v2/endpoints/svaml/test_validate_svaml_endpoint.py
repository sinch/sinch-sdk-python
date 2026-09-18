import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.svaml_endpoints import (
    ValidateSvamlEndpoint,
)
from sinch.domains.voice.models.v2.svaml.internal.request.validate_svaml_request import (
    ValidateSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)


@pytest.fixture
def request_data():
    return ValidateSvamlRequest(
        svaml={"commands": [{"command": "answer"}]},
        validation_type="STRICT",
    )


@pytest.fixture
def endpoint(request_data):
    return ValidateSvamlEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "isValid": False,
            "errors": ["Invalid dial command. Missing destination."],
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
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/svaml/validate",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/svaml/validate"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that all fields serialize correctly to the request body, applying aliases."""
    body = json.loads(endpoint.request_body())

    assert body["svaml"]["commands"][0]["command"] == "answer"
    assert body["validationType"] == "STRICT"
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and an omitted field is absent."""
    endpoint = ValidateSvamlEndpoint(
        "test_project_id",
        ValidateSvamlRequest(
            svaml={"commands": [{"command": "answer"}]},
            validation_type=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["svaml"]["commands"][0]["command"] == "answer"
    assert body["validationType"] is None

    endpoint_without_validation_type = ValidateSvamlEndpoint(
        "test_project_id",
        ValidateSvamlRequest(svaml={"commands": [{"command": "answer"}]}),
    )
    body_without_validation_type = json.loads(
        endpoint_without_validation_type.request_body()
    )
    assert "validationType" not in body_without_validation_type


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ValidateSvamlResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ValidateSvamlResponse)
    assert parsed_response.is_valid is False
    assert parsed_response.errors == [
        "Invalid dial command. Missing destination."
    ]


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
