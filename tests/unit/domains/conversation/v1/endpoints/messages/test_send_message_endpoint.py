import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import SendMessageEndpoint
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.models.v1.messages.internal.request import (
    SendMessageRequest,
    SendMessageRequestBody,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)
from sinch.domains.conversation.models.v1.messages.categories.text import TextMessage
from sinch.domains.conversation.models.v1.messages.response import (
    SendMessageResponse,
)


@pytest.fixture
def request_data():
    return SendMessageRequest(
        app_id="my app ID",
        recipient=Recipient(contact_id="my contact ID"),
        message=SendMessageRequestBody(
            text_message=TextMessage(text="This is a text message.")
        ),
    )


@pytest.fixture
def mock_send_message_response():
    """Mock response for SendMessageResponse."""
    return HTTPResponse(
        status_code=200,
        body={"message_id": "01FC66621XXXXX119Z8PMV1QPQ"},
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    """Mock error response for send message endpoint."""
    return HTTPResponse(
        status_code=400,
        body={
            "error": {
                "code": 400,
                "message": "Invalid argument",
                "status": "INVALID_ARGUMENT"
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return SendMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages:send"
    )


def test_request_body_expects_valid_json_with_app_id_recipient_message(request_data):
    """Test that the endpoint produces a JSON body with app_id, recipient, and message."""
    endpoint = SendMessageEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "my app ID"
    assert body["recipient"]["contact_id"] == "my contact ID"
    assert "text_message" in body["message"]
    assert "project_id" not in body


def test_handle_response_expects_send_message_response(endpoint, mock_send_message_response):
    """Test that SendMessageResponse is handled correctly."""
    parsed_response = endpoint.handle_response(mock_send_message_response)

    assert isinstance(parsed_response, SendMessageResponse)
    assert parsed_response.message_id == "01FC66621XXXXX119Z8PMV1QPQ"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
