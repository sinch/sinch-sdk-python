import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.services_endpoints import (
    GetServiceEndpoint,
)
from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)


@pytest.fixture
def request_data():
    return ServiceIdRequest(service_id="6e124178-c29d-46a5-943c-5c2ae544aade")


@pytest.fixture
def endpoint(request_data):
    return GetServiceEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
            "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            "createTime": "2025-01-01T00:00:00Z",
            "updateTime": "2025-06-01T09:15:00Z",
            "name": "My Voice Service",
            "description": "Service with static call behavior",
            "isDefault": True,
            "callBehavior": {
                "type": "STATIC",
                "static": {"commands": [{"command": "hangup"}]},
            },
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
            "detail": "The service could not be found.",
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


def test_request_body_expects_no_body(endpoint):
    """Test that the dumped body is empty since the only field is a path param."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ServiceResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ServiceResponse)
    assert parsed_response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert parsed_response.update_time is not None
    assert parsed_response.call_behavior.type == "STATIC"
    assert parsed_response.call_behavior.static.commands[0].command == (
        "hangup"
    )


def test_handle_response_expects_voice_exception_on_error(
    endpoint, mock_error_response
):
    """Test that VoiceException is raised when the server returns an error."""
    with pytest.raises(VoiceException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Not Found: The service could not be found."
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
