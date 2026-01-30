"""
Unit tests for Conversation Messages API
"""
from unittest.mock import MagicMock
import pytest
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.api.v1 import Messages
from sinch.domains.conversation.api.v1.internal import (
    DeleteMessageEndpoint,
    GetMessageEndpoint,
    SendMessageEndpoint,
    UpdateMessageMetadataEndpoint,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    MessageIdRequest,
    UpdateMessageMetadataRequest,
    SendMessageRequest,
)
from sinch.domains.conversation.models.v1.messages.response.types import (
    SendMessageResponse,
)


@pytest.fixture
def mock_send_message_response():
    return SendMessageResponse(
        message_id="01FC66621SND04119Z8PMV1QPQ",
    )


@pytest.fixture
def mock_conversation_message_response():
    response = MagicMock()
    response.id = "01FC66621GET02119Z8PMV1QPQ"
    return response


def test_conversation_expects_messages_attribute(mock_sinch_client_conversation):
    """Test that Conversation exposes .messages as Messages instance."""
    conversation = Conversation(mock_sinch_client_conversation)
    assert isinstance(conversation.messages, Messages)


def test_messages_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        None
    )
    spy_endpoint = mocker.spy(DeleteMessageEndpoint, "__init__")

    message_id = "01FC66621DEL01119Z8PMV1QPQ"
    conversation = Conversation(mock_sinch_client_conversation)
    conversation.messages.delete(message_id=message_id)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], MessageIdRequest)
    assert kwargs["request_data"].message_id == message_id
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_delete_with_messages_source_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete with messages_source sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        None
    )
    spy_endpoint = mocker.spy(DeleteMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    message_id = "01FC66621DL205119Z8PMV1QPQ"
    conversation.messages.delete(
        message_id=message_id,
        messages_source="DISPATCH_SOURCE",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["request_data"].message_id == message_id
    assert kwargs["request_data"].messages_source == "DISPATCH_SOURCE"


def test_messages_get_expects_correct_request(
    mock_sinch_client_conversation, mock_conversation_message_response, mocker
):
    """Test that get sends the correct request and returns the response."""
    message_id = "01FC66621GET02119Z8PMV1QPQ"
    mock_conversation_message_response.id = message_id
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_conversation_message_response
    )
    spy_endpoint = mocker.spy(GetMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.get(message_id=message_id)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], MessageIdRequest)
    assert kwargs["request_data"].message_id == message_id
    assert response.id == message_id
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_update_expects_correct_request(
    mock_sinch_client_conversation, mock_conversation_message_response, mocker
):
    """Test that update sends the correct request and returns the response."""
    message_id = "01FC66621UPD03119Z8PMV1QPQ"
    mock_conversation_message_response.id = message_id
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_conversation_message_response
    )
    spy_endpoint = mocker.spy(UpdateMessageMetadataEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.update(
        message_id=message_id,
        metadata="updated-metadata",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], UpdateMessageMetadataRequest)
    assert kwargs["request_data"].message_id == message_id
    assert kwargs["request_data"].metadata == "updated-metadata"
    assert response.id == message_id
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send sends the correct request and returns SendMessageResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send(
        app_id="APP_ID",
        message={"text_message": {"text": "Hello"}},
        recipient_identities=[
            {"channel": "RCS", "identity": "+46701234567"},
        ],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], SendMessageRequest)
    assert kwargs["request_data"].app_id == "APP_ID"
    assert kwargs["request_data"].message.text_message is not None
    assert kwargs["request_data"].message.text_message.text == "Hello"
    assert isinstance(response, SendMessageResponse)
    assert response.message_id == "01FC66621SND04119Z8PMV1QPQ"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_with_contact_id_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send with contact_id builds recipient correctly."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send(
        app_id="APP_ID",
        message={"text_message": {"text": "Hi"}},
        contact_id="CONTACT_123",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert isinstance(kwargs["request_data"], SendMessageRequest)
    assert kwargs["request_data"].app_id == "APP_ID"
    assert kwargs["request_data"].recipient.contact_id == "CONTACT_123"
    assert isinstance(response, SendMessageResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_text_message_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send_text_message sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send_text_message(
        app_id="APP_ID",
        text="Hello",
        recipient_identities=[
            {"channel": "RCS", "identity": "+46701234567"},
        ],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert isinstance(kwargs["request_data"], SendMessageRequest)
    assert kwargs["request_data"].app_id == "APP_ID"
    assert kwargs["request_data"].message.text_message is not None
    assert kwargs["request_data"].message.text_message.text == "Hello"
    assert isinstance(response, SendMessageResponse)
    assert response.message_id == "01FC66621SND04119Z8PMV1QPQ"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_card_message_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send_card_message sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send_card_message(
        app_id="APP_ID",
        card_message={"title": "Card title", "description": "Description"},
        recipient_identities=[
            {"channel": "RCS", "identity": "+46701234567"},
        ],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert isinstance(kwargs["request_data"], SendMessageRequest)
    assert kwargs["request_data"].app_id == "APP_ID"
    assert kwargs["request_data"].message.card_message is not None
    assert kwargs["request_data"].message.card_message.title == "Card title"
    assert isinstance(response, SendMessageResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_choice_message_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send_choice_message sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send_choice_message(
        app_id="APP_ID",
        choice_message={
            "text_message": {"text": "Choose:"},
            "choices": [
                {"text_message": {"text": "Option A"}, "postback_data": "a"},
            ],
        },
        recipient_identities=[
            {"channel": "RCS", "identity": "+46701234567"},
        ],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert isinstance(kwargs["request_data"], SendMessageRequest)
    assert kwargs["request_data"].app_id == "APP_ID"
    assert kwargs["request_data"].message.choice_message is not None
    assert kwargs["request_data"].message.choice_message.text_message.text == "Choose:"
    assert len(kwargs["request_data"].message.choice_message.choices) == 1
    assert isinstance(response, SendMessageResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_messages_send_media_message_expects_correct_request(
    mock_sinch_client_conversation, mock_send_message_response, mocker
):
    """Test that send_media_message sends the correct request."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_send_message_response
    )
    spy_endpoint = mocker.spy(SendMessageEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.messages.send_media_message(
        app_id="APP_ID",
        media_message={"url": "https://example.com/image.jpg"},
        recipient_identities=[
            {"channel": "RCS", "identity": "+46701234567"},
        ],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["request_data"].message.media_message is not None
    assert kwargs["request_data"].message.media_message.url == "https://example.com/image.jpg"
    assert isinstance(response, SendMessageResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
