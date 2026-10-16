import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.events_endpoints import (
    ListEventsEndpoint,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_request import (
    ListEventsRequest,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_response import (
    ListEventsResponse,
)
from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)


@pytest.fixture
def request_data():
    return ListEventsRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        page_size=5,
        page_token="token_abc",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "events": [
                {
                    "id": "01W4FFL35P4NC4K35EVENT0001",
                    "app_event": {"composing_event": {}},
                    "channel_identity": {
                        "channel": "SMS",
                        "identity": "46700000000",
                    },
                    "processing_mode": "CONVERSATION",
                },
                {
                    "id": "01W4FFL35P4NC4K35EVENT0002",
                    "app_event": {"read_message_event": {}},
                    "channel_identity": {
                        "channel": "SMS",
                        "identity": "46700000000",
                    },
                    "processing_mode": "CONVERSATION",
                },
            ],
            "next_page_token": "token_next_page_abc",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=400,
        body={
            "error": {
                "code": 400,
                "message": "Invalid argument",
                "status": "INVALID_ARGUMENT",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListEventsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly (no path params beyond project_id)."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/events"
    )


def test_build_query_params_expects_parsed_params(endpoint):
    """Test that all query param fields are serialized when set."""
    assert endpoint.build_query_params() == {
        "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "page_size": 5,
        "page_token": "token_abc",
    }


def test_build_query_params_expects_excludes_unset_fields():
    """Test that query params only include non-None fields."""
    endpoint = ListEventsEndpoint(
        "test_project_id", ListEventsRequest(contact_id="CONTACT123")
    )

    assert endpoint.build_query_params() == {"contact_id": "CONTACT123"}


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ListEventsResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListEventsResponse)
    assert len(parsed_response.content) == 2
    assert isinstance(parsed_response.content[0], ConversationEventResponse)
    assert parsed_response.content[1].id == "01W4FFL35P4NC4K35EVENT0002"
    assert parsed_response.next_page_token == "token_next_page_abc"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
