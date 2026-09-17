import uuid

import pytest

from sinch.core.pagination import LinkBasedPaginator
from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.internal.services_endpoints import (
    CreateServiceEndpoint,
    DeleteServiceEndpoint,
    GetServiceEndpoint,
    ListServicesEndpoint,
    UpdateServiceEndpoint,
)
from sinch.domains.voice.api.v2.services_apis import Services
from sinch.domains.voice.models.v2.services.internal.list_services_response import (
    ListServicesResponse,
)
from sinch.domains.voice.models.v2.services.internal.request.create_service_request import (
    CreateServiceRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.list_services_request import (
    ListServicesRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.update_service_request import (
    UpdateServiceRequest,
)
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)
from sinch.domains.voice.models.v2.services.response.service_short_response import ServiceShortResponse
from sinch.domains.voice.models.v2.shared.pagination_links import (
    PaginationLinks,
)
from sinch.domains.voice.models.v2.shared.pagination_meta import (
    PaginationMeta,
)


def test_voice_exposes_v2_services(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned services resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.services, Services)


@pytest.fixture
def mock_list_services_response():
    return ListServicesResponse(
        services=[
            ServiceShortResponse(
                service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
                project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
                create_time="2025-01-01T00:00:00Z",
                name="Example service",
                is_default=False,
            )
        ],
        links=PaginationLinks(
            first="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=1",
            last="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=2&pageSize=1",
            next="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=2&pageSize=1",
            self="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=1",
        ),
        meta=PaginationMeta(totalCount=2, pageCount=2),
    )


def test_services_list_expects_correct_request(
    mock_sinch_client_voice, mock_list_services_response, mocker
):
    """Test that all parameters of list are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        mock_list_services_response
    )
    spy = mocker.spy(ListServicesEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.services.list(
        filter="example",
        is_default=True,
        page_size=1,
        page=1,
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ListServicesRequest)
    assert request_data.filter == "example"
    assert request_data.is_default is True
    assert request_data.page_size == 1
    assert request_data.page == 1
    assert isinstance(response, LinkBasedPaginator)
    assert response.result == mock_list_services_response
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_services_create_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that all parameters of create are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        ServiceResponse(
            serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
            projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            createTime="2025-01-01T00:00:00Z",
            name="Example service",
            isDefault=False,
        )
    )
    spy = mocker.spy(CreateServiceEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.services.create(
        name="Example service",
        description="Service with custom events",
        is_default=False,
        call_behavior={
            "type": "EVENT_DESTINATION",
            "event_destination": {
                "url": "https://example.com/event_destination",
                "fallback_url": "https://example.com/fallback",
            },
        },
        idempotency_key="my-custom-key",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, CreateServiceRequest)
    assert request_data.name == "Example service"
    assert request_data.description == "Service with custom events"
    assert request_data.is_default is False
    assert request_data.call_behavior.type == "EVENT_DESTINATION"
    assert (
        request_data.call_behavior.event_destination.url
        == "https://example.com/event_destination"
    )
    assert request_data.idempotency_key == "my-custom-key"
    assert isinstance(response, ServiceResponse)
    assert response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_services_create_expects_omitted_optionals_unset(
    mock_sinch_client_voice, mocker
):
    """Test that omitted optional fields never reach the request model."""
    spy = mocker.spy(CreateServiceEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.services.create(name="Example service")

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert "description" not in request_data.model_fields_set
    assert "is_default" not in request_data.model_fields_set
    assert "call_behavior" not in request_data.model_fields_set
    assert uuid.UUID(request_data.idempotency_key).version == 4


def test_services_get_expects_correct_request(mock_sinch_client_voice, mocker):
    """Test that service_id is mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        ServiceResponse(
            serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
            projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            createTime="2025-01-01T00:00:00Z",
            name="Example service",
            isDefault=True,
        )
    )
    spy = mocker.spy(GetServiceEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.services.get(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ServiceIdRequest)
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert isinstance(response, ServiceResponse)
    assert response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_services_update_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that all parameters of update are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        ServiceResponse(
            serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
            projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            createTime="2025-01-01T00:00:00Z",
            name="Renamed service",
            isDefault=True,
        )
    )
    spy = mocker.spy(UpdateServiceEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.services.update(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        name="Renamed service",
        description=None,
        is_default=True,
        call_behavior={"type": "NONE"},
        idempotency_key="my-custom-key",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, UpdateServiceRequest)
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert request_data.name == "Renamed service"
    assert request_data.description is None
    assert request_data.is_default is True
    assert request_data.call_behavior.type == "NONE"
    assert request_data.idempotency_key == "my-custom-key"
    assert isinstance(response, ServiceResponse)
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_services_update_expects_omitted_optionals_unset(
    mock_sinch_client_voice, mocker
):
    """Test that omitted optional fields never reach the request model."""
    spy = mocker.spy(UpdateServiceEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.services.update(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade"
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert "name" not in request_data.model_fields_set
    assert "description" not in request_data.model_fields_set
    assert "is_default" not in request_data.model_fields_set
    assert "call_behavior" not in request_data.model_fields_set


def test_services_delete_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that service_id is mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = None
    spy = mocker.spy(DeleteServiceEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.services.delete(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ServiceIdRequest)
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert response is None
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()
