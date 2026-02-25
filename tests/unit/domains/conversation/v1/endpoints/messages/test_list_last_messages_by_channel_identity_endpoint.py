import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import (
    ListLastMessagesByChannelIdentityEndpoint,
)
from sinch.domains.conversation.models.v1.messages.internal import (
    ListMessagesResponse,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListLastMessagesByChannelIdentityRequest,
)
from tests.unit.domains.conversation.v1.models.response.test_conversation_message_response_model import (
    contact_message_response_data,
)


@pytest.fixture
def request_data():
    return ListLastMessagesByChannelIdentityRequest(
        channel_identities=["+15551234567"],
        messages_source="DISPATCH_SOURCE",
        page_size=2,
    )


@pytest.fixture
def endpoint(request_data):
    return ListLastMessagesByChannelIdentityEndpoint(
        "test_project_id", request_data
    )


@pytest.fixture
def mock_list_last_messages_response(contact_message_response_data):
    return HTTPResponse(
        status_code=200,
        body={
            "messages": [contact_message_response_data],
            "next_page_token": "token_next_page_abc",
        },
        headers={"Content-Type": "application/json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages:fetch-last-message"
    )


def test_request_body_expects_parsed_params():
    """Test that all body fields are serialized when set."""
    request_data = ListLastMessagesByChannelIdentityRequest(
        channel_identities=["+46701234567", "+46709876543"],
        contact_ids=["CONTACT123"],
        app_id="APP789",
        messages_source="DISPATCH_SOURCE",
        page_size=20,
        page_token="token_xyz",
        view="WITH_METADATA",
        channel="WHATSAPP",
        direction="TO_APP",
    )
    endpoint = ListLastMessagesByChannelIdentityEndpoint(
        "test_project_id", request_data
    )
    body = json.loads(endpoint.request_body())

    assert body["channel_identities"] == ["+46701234567", "+46709876543"]
    assert body["contact_ids"] == ["CONTACT123"]
    assert body["app_id"] == "APP789"
    assert body["messages_source"] == "DISPATCH_SOURCE"
    assert body["page_size"] == 20
    assert body["page_token"] == "token_xyz"
    assert body["view"] == "WITH_METADATA"
    assert body["channel"] == "WHATSAPP"
    assert body["direction"] == "TO_APP"


def test_handle_response_expects_list_messages_response(
    endpoint, mock_list_last_messages_response
):
    """Test that a successful response is parsed to ListMessagesResponse."""
    result = endpoint.handle_response(mock_list_last_messages_response)

    assert isinstance(result, ListMessagesResponse)
    assert result.next_page_token == "token_next_page_abc"
    assert result.messages is not None
    assert len(result.messages) == 1
    assert result.messages[0].id == "CAPY123456789ABCDEFGHIJKLMNOP"


def test_handle_response_expects_empty_messages_list():
    """Test that response with empty messages list is handled correctly."""
    request_data = ListLastMessagesByChannelIdentityRequest(page_size=10)
    endpoint = ListLastMessagesByChannelIdentityEndpoint(
        "test_project_id", request_data
    )
    mock_response = HTTPResponse(
        status_code=200,
        body={"messages": [], "next_page_token": None},
        headers={"Content-Type": "application/json"},
    )

    result = endpoint.handle_response(mock_response)

    assert isinstance(result, ListMessagesResponse)
    assert result.messages == []
    assert result.next_page_token is None
