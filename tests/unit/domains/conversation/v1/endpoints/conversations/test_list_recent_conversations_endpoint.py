from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    ListRecentConversationsEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_request import (
    ListRecentConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_response import (
    ListRecentConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.recent_conversation_response import (
    RecentConversationResponse,
)
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TextAppMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    MediaContactMessage,
)
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


@pytest.fixture
def request_data():
    return ListRecentConversationsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        only_active=True,
        page_size=5,
        page_token="token_abc",
        order="ASC",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "conversations": [
                {
                    "conversation": {
                        "id": "01W4FFL35P4NC4K35CONVERS001",
                        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
                        "active": True,
                        "active_channel": "MESSENGER",
                        "last_received": "2026-10-09T10:00:00Z",
                    },
                    "last_message": {
                        "id": "01W4FFL35P4NC4K35MESSAGE001",
                        "direction": "TO_CONTACT",
                        "app_message": {"text_message": {"text": "Hello"}},
                        "channel_identity": {
                            "channel": "MESSENGER",
                            "identity": "7595725018225506",
                        },
                        "conversation_id": "01W4FFL35P4NC4K35CONVERS001",
                        "accept_time": "2026-10-09T10:00:00Z",
                        "injected": False,
                    },
                },
                {
                    "conversation": {
                        "id": "01W4FFL35P4NC4K35CONVERS002",
                        "active": False,
                    },
                    "last_message": {
                        "id": "01W4FFL35P4NC4K35MESSAGE002",
                        "direction": "TO_APP",
                        "contact_message": {
                            "media_message": {
                                "url": "https://example.com/image.png"
                            }
                        },
                    },
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
    return ListRecentConversationsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the :recent custom verb."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations:recent"
    )


def test_build_query_params_expects_parsed_params(endpoint):
    """Test that all query param fields are serialized when set."""
    assert endpoint.build_query_params() == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "only_active": True,
        "page_size": 5,
        "page_token": "token_abc",
        "order": "ASC",
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that fields passed as None are excluded from the query params."""
    endpoint = ListRecentConversationsEndpoint(
        "test_project_id",
        ListRecentConversationsRequest(app_id="APP123", order=None),
    )

    assert endpoint.build_query_params() == {"app_id": "APP123"}


def test_build_query_params_expects_extra_fields_excluded():
    """Test that unknown extra fields are not sent as query params."""
    endpoint = ListRecentConversationsEndpoint(
        "test_project_id",
        ListRecentConversationsRequest(app_id="APP123", unknown_field="x"),
    )

    assert endpoint.build_query_params() == {"app_id": "APP123"}


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ListRecentConversationsResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListRecentConversationsResponse)
    assert len(parsed_response.content) == 2
    first = parsed_response.content[0]
    assert isinstance(first, RecentConversationResponse)
    assert isinstance(first.conversation, ConversationResponse)
    assert first.conversation.id == "01W4FFL35P4NC4K35CONVERS001"
    assert first.conversation.active_channel == "MESSENGER"
    assert first.conversation.last_received == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
    assert first.last_message.id == "01W4FFL35P4NC4K35MESSAGE001"
    assert first.last_message.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert first.last_message.injected is False
    assert parsed_response.next_page_token == "token_next_page_abc"
    assert parsed_response.total_size == 2
    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_last_message_union_resolved(
    endpoint, mock_response
):
    """Test that last_message resolves to the app or contact message variant."""
    parsed_response = endpoint.handle_response(mock_response)

    app_last_message = parsed_response.content[0].last_message
    assert isinstance(app_last_message, AppMessageResponse)
    assert isinstance(app_last_message.app_message, TextAppMessage)
    assert app_last_message.app_message.text_message.text == "Hello"
    contact_last_message = parsed_response.content[1].last_message
    assert isinstance(contact_last_message, ContactMessageResponse)
    assert isinstance(
        contact_last_message.contact_message, MediaContactMessage
    )


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
