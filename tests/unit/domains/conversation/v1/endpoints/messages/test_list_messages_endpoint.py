import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import ListMessagesEndpoint
from sinch.domains.conversation.models.v1.messages.internal import (
    ListMessagesResponse,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListMessagesRequest,
)
from tests.unit.domains.conversation.v1.models.response.test_conversation_message_response_model import (
    contact_message_response_data,
)


@pytest.fixture
def request_data():
    return ListMessagesRequest(page_size=10)


@pytest.fixture
def endpoint(request_data):
    return ListMessagesEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_list_messages_response(contact_message_response_data):
    return HTTPResponse(
        status_code=200,
        body={
            "messages": [contact_message_response_data],
            "next_page_token": "token_next_page_abc",
        },
        headers={"Content-Type": "application/json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly (no path params beyond project_id)."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages"
    )


def test_build_query_params_expects_excludes_unset_fields():
    """Test that query params only include non-None fields."""
    request_data = ListMessagesRequest(page_size=10)
    endpoint = ListMessagesEndpoint("test_project_id", request_data)

    query_params = endpoint.build_query_params()

    assert query_params["page_size"] == 10
    assert "conversation_id" not in query_params


def test_build_query_params_expects_parsed_params():
    """Test that all query param fields are serialized when set."""
    request_data = ListMessagesRequest(
        conversation_id="CONV123",
        contact_id="CONTACT456",
        app_id="APP789",
        channel_identity="+46701234567",
        page_size=20,
        page_token="token_xyz",
        view="WITH_METADATA",
        messages_source="DISPATCH_SOURCE",
        only_recipient_originated=True,
        channel="WHATSAPP",
        direction="TO_APP",
    )
    endpoint = ListMessagesEndpoint("test_project_id", request_data)

    query_params = endpoint.build_query_params()

    assert query_params["conversation_id"] == "CONV123"
    assert query_params["contact_id"] == "CONTACT456"
    assert query_params["app_id"] == "APP789"
    assert query_params["channel_identity"] == "+46701234567"
    assert query_params["page_size"] == 20
    assert query_params["page_token"] == "token_xyz"
    assert query_params["view"] == "WITH_METADATA"
    assert query_params["messages_source"] == "DISPATCH_SOURCE"
    assert query_params["only_recipient_originated"] is True
    assert query_params["channel"] == "WHATSAPP"
    assert query_params["direction"] == "TO_APP"


def test_handle_response_expects_list_messages_response(
    endpoint, mock_list_messages_response
):
    """Test that a successful response is parsed to ListMessagesResponse."""
    result = endpoint.handle_response(mock_list_messages_response)

    assert isinstance(result, ListMessagesResponse)
    assert result.next_page_token == "token_next_page_abc"
    assert result.messages is not None
    assert len(result.messages) == 1
    assert result.messages[0].id == "CAPY123456789ABCDEFGHIJKLMNOP"


def test_handle_response_expects_empty_messages_list():
    """Test that response with empty messages list is handled correctly."""
    request_data = ListMessagesRequest(page_size=10)
    endpoint = ListMessagesEndpoint("test_project_id", request_data)
    mock_response = HTTPResponse(
        status_code=200,
        body={"messages": [], "next_page_token": None},
        headers={"Content-Type": "application/json"},
    )

    result = endpoint.handle_response(mock_response)

    assert isinstance(result, ListMessagesResponse)
    assert result.messages == []
    assert result.next_page_token is None
