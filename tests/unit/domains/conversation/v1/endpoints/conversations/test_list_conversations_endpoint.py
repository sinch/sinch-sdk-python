import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    ListConversationsEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_request import (
    ListConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_response import (
    ListConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)


@pytest.fixture
def request_data():
    return ListConversationsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        only_active=True,
        page_size=5,
        page_token="token_abc",
        active_channel="WHATSAPP",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "conversations": [
                {
                    "id": "01W4FFL35P4NC4K35CONVERS001",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                    "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                    "active": True,
                    "active_channel": "WHATSAPP",
                },
                {
                    "id": "01W4FFL35P4NC4K35CONVERS002",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                    "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                    "active": False,
                    "active_channel": "SMS",
                },
            ],
            "next_page_token": "token_next_page_abc",
            "total_size": 2,
            "unexpected_field": "kept",
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
    return ListConversationsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly (no path params beyond project_id)."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations"
    )


def test_build_query_params_expects_parsed_params(endpoint):
    """Test that all query param fields are serialized when set."""
    assert endpoint.build_query_params() == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "only_active": True,
        "page_size": 5,
        "page_token": "token_abc",
        "active_channel": "WHATSAPP",
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that fields passed as None are excluded from the query params."""
    endpoint = ListConversationsEndpoint(
        "test_project_id",
        ListConversationsRequest(app_id="APP123", contact_id=None),
    )

    assert endpoint.build_query_params() == {"app_id": "APP123"}


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ListConversationsResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListConversationsResponse)
    assert len(parsed_response.content) == 2
    assert isinstance(parsed_response.content[0], ConversationResponse)
    assert parsed_response.content[0].active_channel == "WHATSAPP"
    assert parsed_response.content[1].id == "01W4FFL35P4NC4K35CONVERS002"
    assert parsed_response.content[1].active is False
    assert parsed_response.next_page_token == "token_next_page_abc"
    assert parsed_response.total_size == 2
    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
