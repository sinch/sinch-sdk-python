import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.events_endpoints import (
    GetEventEndpoint,
)
from sinch.domains.conversation.models.v1.events.internal.event_id_request import (
    EventIdRequest,
)
from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    GenericAppEvent,
)


@pytest.fixture
def request_data():
    return EventIdRequest(event_id="01W4FFL35P4NC4K35EVENT0001")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35EVENT0001",
            "direction": "TO_CONTACT",
            "app_event": {"generic_event": {"payload": {"key": "value"}}},
            "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
            "contact_id": "01W4FFL35P4NC4K35CONTACT001",
            "channel_identity": {
                "channel": "SMS",
                "identity": "46700000000",
                "app_id": "",
            },
            "accept_time": "2026-10-09T10:00:00Z",
            "processing_mode": "CONVERSATION",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "code": 404,
                "message": "Not found",
                "status": "NOT_FOUND",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetEventEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the event ID path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/events/01W4FFL35P4NC4K35EVENT0001"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ConversationEventResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ConversationEventResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35EVENT0001"
    assert parsed_response.direction == "TO_CONTACT"
    assert isinstance(parsed_response.app_event, GenericAppEvent)
    assert parsed_response.app_event.generic_event.payload == {"key": "value"}
    assert parsed_response.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert parsed_response.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert parsed_response.channel_identity.channel == "SMS"
    assert parsed_response.processing_mode == "CONVERSATION"
    assert parsed_response.accept_time.year == 2026


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
