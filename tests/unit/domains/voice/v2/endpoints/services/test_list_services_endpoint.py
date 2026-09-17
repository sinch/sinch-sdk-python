import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.services_endpoints import (
    ListServicesEndpoint,
)
from sinch.domains.voice.models.v2.services.internal.list_services_response import (
    ListServicesResponse,
)
from sinch.domains.voice.models.v2.services.internal.request.list_services_request import (
    ListServicesRequest,
)


@pytest.fixture
def request_data():
    return ListServicesRequest(
        filter="Primary",
        is_default=True,
        page_size=1,
        page=2,
    )


@pytest.fixture
def endpoint(request_data):
    return ListServicesEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "services": [
                {
                    "serviceId": "6e124178-c29d-46a5-943c-5c2ae544aade",
                    "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
                    "createTime": "2025-01-01T00:00:00Z",
                    "name": "Primary Service",
                    "description": "Main service",
                    "isDefault": True,
                }
            ],
            "links": {
                "first": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=1",
                "last": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=1",
                "self": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=1",
            },
            "meta": {"totalCount": 1, "pageCount": 1},
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
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_voice)
        == "https://voice.api.sinch.com/v2/projects/test_project_id/services"
    )


def test_build_query_params_expects_correct_serialization(endpoint):
    """Test that all query fields serialize correctly, applying aliases."""
    assert endpoint.build_query_params() == {
        "filter": "Primary",
        "isDefault": True,
        "pageSize": 1,
        "page": 2,
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that fields passed as None are excluded from the query params."""
    endpoint = ListServicesEndpoint("test_project_id", ListServicesRequest())

    assert endpoint.build_query_params() == {}


def test_request_body_expects_no_body(endpoint):
    """Test that the dumped body is empty since every field is a query param."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ListServicesResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListServicesResponse)
    assert len(parsed_response.services) == 1
    assert (
        parsed_response.services[0].service_id
        == "6e124178-c29d-46a5-943c-5c2ae544aade"
    )
    assert parsed_response.content == parsed_response.services
    assert parsed_response.meta.total_count == 1
    assert parsed_response.meta.page_count == 1


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
