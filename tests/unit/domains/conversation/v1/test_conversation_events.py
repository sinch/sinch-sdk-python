"""
Unit tests for Conversation Events API
"""

import pytest

from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1 import Events
from sinch.domains.conversation.api.v1.internal.events_endpoints import (
    DeleteEventEndpoint,
    GetEventEndpoint,
    ListEventsEndpoint,
    SendEventEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.events.internal.event_id_request import (
    EventIdRequest,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_request import (
    ListEventsRequest,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_response import (
    ListEventsResponse,
)
from sinch.domains.conversation.models.v1.events.internal.send_event_request import (
    SendEventRequest,
)
from sinch.domains.conversation.models.v1.events.response.send_event_response import (
    SendEventResponse,
)

APP_ID = "01W4FFL35P4NC4K35CONVAPP001"
EVENT_ID = "01W4FFL35P4NC4K35EVENT0001"
CONTACT_ID = "01W4FFL35P4NC4K35CONTACT001"


@pytest.fixture
def mock_send_event_response():
    return SendEventResponse(event_id=EVENT_ID)


def test_conversation_expects_events_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .events as an Events instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.events, Events)


def test_events_send_expects_correct_request(
    mock_sinch_client_conversation, mock_send_event_response, mocker
):
    """Test that send builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_send_event_response
    spy_endpoint = mocker.spy(SendEventEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).events.send(
        app_id=APP_ID,
        event={"composing_event": {}},
        contact_id=CONTACT_ID,
        event_destination_target="https://my-server.com/events",
        channel_priority_order=["WHATSAPP"],
        event_metadata="metadata",
        queue="HIGH_PRIORITY",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, SendEventRequest)
    assert request_data.app_id == APP_ID
    assert request_data.event.composing_event is not None
    assert request_data.recipient.contact_id == CONTACT_ID
    assert (
        request_data.event_destination_target
        == "https://my-server.com/events"
    )
    assert request_data.channel_priority_order == ["WHATSAPP"]
    assert request_data.event_metadata == "metadata"
    assert request_data.queue == "HIGH_PRIORITY"
    assert response is mock_send_event_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_events_send_expects_recipient_identities_as_identified_by(
    mock_sinch_client_conversation, mock_send_event_response, mocker
):
    """Test that recipient_identities are wrapped in the identified_by recipient."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_send_event_response
    spy_endpoint = mocker.spy(SendEventEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).events.send(
        app_id=APP_ID,
        event={"generic_event": {"payload": {"key": "value"}}},
        recipient_identities=[{"channel": "SMS", "identity": "46700000000"}],
    )

    _, kwargs = spy_endpoint.call_args
    recipient = kwargs["request_data"].recipient
    assert recipient.identified_by.channel_identities[0].channel == "SMS"
    assert (
        recipient.identified_by.channel_identities[0].identity
        == "46700000000"
    )


def test_events_send_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_send_event_response, mocker
):
    """Test that omitted parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_send_event_response
    spy_endpoint = mocker.spy(SendEventEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).events.send(
        app_id=APP_ID,
        event={"composing_event": {}},
        contact_id=CONTACT_ID,
        event_metadata=None,
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert request_data.model_fields_set == {
        "app_id",
        "event",
        "recipient",
        "event_metadata",
    }
    assert request_data.event_metadata is None


def test_events_send_expects_value_error_without_recipient(
    mock_sinch_client_conversation,
):
    """Test that send requires either contact_id or recipient_identities."""
    with pytest.raises(ValueError):
        Conversation(mock_sinch_client_conversation).events.send(
            app_id=APP_ID, event={"composing_event": {}}
        )


def test_events_get_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that get builds the request model and returns the response."""
    mock_response = object()
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(GetEventEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).events.get(
        event_id=EVENT_ID
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], EventIdRequest)
    assert kwargs["request_data"].event_id == EVENT_ID
    assert response is mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_events_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete builds the request model and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteEventEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).events.delete(
        event_id=EVENT_ID
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], EventIdRequest)
    assert kwargs["request_data"].event_id == EVENT_ID
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_events_list_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list builds the request model and returns a TokenBasedPaginator."""
    mock_response = ListEventsResponse(events=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListEventsEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).events.list(
        conversation_id="CONV123", contact_id=CONTACT_ID, page_size=5
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ListEventsRequest)
    assert request_data.conversation_id == "CONV123"
    assert request_data.contact_id == CONTACT_ID
    assert request_data.page_size == 5
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
