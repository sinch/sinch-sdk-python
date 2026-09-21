import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.services_endpoints import (
    UpdateServiceEndpoint,
)
from sinch.domains.voice.models.v2.services.internal.request.update_service_request import (
    UpdateServiceRequest,
)
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)


@pytest.fixture
def request_data():
    return UpdateServiceRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        name="Renamed service",
        is_default=True,
        call_behavior={"type": "NONE"},
        idempotency_key="my-custom-key",
    )


@pytest.fixture
def endpoint(request_data):
    return UpdateServiceEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
            "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            "createTime": "2025-01-01T00:00:00Z",
            "name": "Renamed service",
            "isDefault": True,
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
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services/6e124178-c29d-46a5-943c-5c2ae544aade",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/services/"
        "6e124178-c29d-46a5-943c-5c2ae544aade"
    )


def test_build_headers_expects_correct_serialization(endpoint):
    """Test that headers defined in the endpoint are correctly built."""
    assert endpoint.build_headers() == {"Idempotency-Key": "my-custom-key"}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that all fields serialize correctly to the request body, applying aliases."""
    body = json.loads(endpoint.request_body())

    assert body["name"] == "Renamed service"
    assert body["isDefault"] is True
    assert body["callBehavior"] == {"type": "NONE"}


def test_request_body_expects_path_params_and_headers_excluded(endpoint):
    """Test that path params and headers never leak into the body."""
    body = json.loads(endpoint.request_body())

    assert "serviceId" not in body
    assert "service_id" not in body
    assert "Idempotency-Key" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and an omitted field is absent."""
    endpoint = UpdateServiceEndpoint(
        "test_project_id",
        UpdateServiceRequest(
            service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
            name="Renamed service",
            description=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["name"] == "Renamed service"
    assert body["description"] is None
    assert "isDefault" not in body
    assert "callBehavior" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ServiceResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ServiceResponse)
    assert parsed_response.name == "Renamed service"
    assert parsed_response.is_default is True


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
