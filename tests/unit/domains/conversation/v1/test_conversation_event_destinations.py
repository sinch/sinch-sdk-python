"""
Unit tests for Conversation Event Destinations API
"""

import pytest

from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1 import EventDestinations
from sinch.domains.conversation.api.v1.internal.event_destinations_endpoints import (
    CreateEventDestinationEndpoint,
    DeleteEventDestinationEndpoint,
    GetEventDestinationEndpoint,
    ListEventDestinationsEndpoint,
    UpdateEventDestinationEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.event_destination_id_request import (
    EventDestinationIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.list_event_destinations_response import (
    ListEventDestinationsResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.request.create_event_destination_request import (
    CreateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.request.update_event_destination_request import (
    UpdateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)

EVENT_DESTINATION_ID = "01W4FFL35P4NC4K35WEBHOOK001"
APP_ID = "01W4FFL35P4NC4K35CONVAPP001"


@pytest.fixture
def mock_event_destination_response():
    return EventDestinationResponse(
        id=EVENT_DESTINATION_ID,
        app_id=APP_ID,
        target="https://my-server.com/events",
    )


def test_conversation_expects_event_destinations_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .event_destinations as an EventDestinations instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.event_destinations, EventDestinations)


def test_event_destinations_create_expects_correct_request(
    mock_sinch_client_conversation, mock_event_destination_response, mocker
):
    """Test that create builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_event_destination_response
    spy_endpoint = mocker.spy(CreateEventDestinationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).event_destinations.create(
        app_id=APP_ID,
        target="https://my-server.com/events",
        client_credentials={
            "endpoint": "https://my-auth-server.com/oauth2/token",
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
            "token_request_type": "FORM",
        },
        secret="my-secret",
        target_type="HTTP",
        triggers=["CAPABILITY", "OPT_IN"],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, CreateEventDestinationRequest)
    assert request_data.app_id == APP_ID
    assert request_data.target == "https://my-server.com/events"
    assert isinstance(request_data.client_credentials, ClientCredentials)
    assert request_data.client_credentials.client_id == "my-client-id"
    assert request_data.client_credentials.token_request_type == "FORM"
    assert request_data.secret == "my-secret"
    assert request_data.target_type == "HTTP"
    assert request_data.triggers == ["CAPABILITY", "OPT_IN"]
    assert response is mock_event_destination_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_event_destinations_create_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_event_destination_response, mocker
):
    """Test that omitted optional parameters are not set on the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_event_destination_response
    spy_endpoint = mocker.spy(CreateEventDestinationEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).event_destinations.create(
        app_id=APP_ID, target="https://my-server.com/events"
    )

    _, kwargs = spy_endpoint.call_args
    assert kwargs["request_data"].model_fields_set == {"app_id", "target"}


def test_event_destinations_list_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list builds the request model and returns a TokenBasedPaginator."""
    mock_response = ListEventDestinationsResponse(webhooks=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListEventDestinationsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).event_destinations.list(app_id=APP_ID)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], AppIdRequest)
    assert kwargs["request_data"].app_id == APP_ID
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_event_destinations_get_expects_correct_request(
    mock_sinch_client_conversation, mock_event_destination_response, mocker
):
    """Test that get builds the request model and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_event_destination_response
    spy_endpoint = mocker.spy(GetEventDestinationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).event_destinations.get(event_destination_id=EVENT_DESTINATION_ID)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], EventDestinationIdRequest)
    assert kwargs["request_data"].event_destination_id == EVENT_DESTINATION_ID
    assert response is mock_event_destination_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_event_destinations_update_expects_correct_request(
    mock_sinch_client_conversation, mock_event_destination_response, mocker
):
    """Test that update builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_event_destination_response
    spy_endpoint = mocker.spy(UpdateEventDestinationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).event_destinations.update(
        event_destination_id=EVENT_DESTINATION_ID,
        app_id=APP_ID,
        target="https://my-server.com/events",
        client_credentials={
            "endpoint": "https://my-auth-server.com/oauth2/token",
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
        secret="my-secret",
        target_type="HTTP",
        triggers=["CAPABILITY"],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, UpdateEventDestinationRequest)
    assert request_data.event_destination_id == EVENT_DESTINATION_ID
    assert request_data.app_id == APP_ID
    assert request_data.target == "https://my-server.com/events"
    assert isinstance(request_data.client_credentials, ClientCredentials)
    assert request_data.secret == "my-secret"
    assert request_data.target_type == "HTTP"
    assert request_data.triggers == ["CAPABILITY"]
    assert response is mock_event_destination_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_event_destinations_update_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_event_destination_response, mocker
):
    """Test that omitted parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_event_destination_response
    spy_endpoint = mocker.spy(UpdateEventDestinationEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).event_destinations.update(
        event_destination_id=EVENT_DESTINATION_ID, secret=None
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert request_data.model_fields_set == {"event_destination_id", "secret"}
    assert request_data.secret is None


def test_event_destinations_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete builds the request model and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteEventDestinationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).event_destinations.delete(event_destination_id=EVENT_DESTINATION_ID)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], EventDestinationIdRequest)
    assert kwargs["request_data"].event_destination_id == EVENT_DESTINATION_ID
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
