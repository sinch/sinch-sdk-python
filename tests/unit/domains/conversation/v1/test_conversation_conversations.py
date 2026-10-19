"""
Unit tests for Conversation Conversations API
"""

from datetime import datetime, timezone

import pytest

from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1 import Conversations
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    CreateConversationEndpoint,
    DeleteConversationEndpoint,
    GetConversationEndpoint,
    InjectEventEndpoint,
    InjectMessageEndpoint,
    ListConversationsEndpoint,
    ListRecentConversationsEndpoint,
    StopActiveConversationEndpoint,
    UpdateConversationEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.conversations.internal.conversation_id_request import (
    ConversationIdRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.create_conversation_request import (
    CreateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_event_request import (
    InjectEventRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_message_request import (
    InjectMessageRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_request import (
    ListConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_response import (
    ListConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_request import (
    ListRecentConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_response import (
    ListRecentConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.internal.update_conversation_request import (
    UpdateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.inject_event_response import (
    InjectEventResponse,
)
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    GenericAppEvent,
)
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TextAppMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    TextContactMessage,
)

APP_ID = "01W4FFL35P4NC4K35CONVAPP001"
CONTACT_ID = "01W4FFL35P4NC4K35CONTACT001"
CONVERSATION_ID = "01W4FFL35P4NC4K35CONVERS001"
ACCEPT_TIME = datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def mock_conversation_response():
    return ConversationResponse(
        id=CONVERSATION_ID, app_id=APP_ID, contact_id=CONTACT_ID
    )


def test_conversation_expects_conversations_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .conversations as a Conversations instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.conversations, Conversations)


def test_conversations_list_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list builds the request model and returns a TokenBasedPaginator."""
    mock_response = ListConversationsResponse(conversations=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListConversationsEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).conversations.list(
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        only_active=True,
        page_size=5,
        page_token="token_abc",
        active_channel="WHATSAPP",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ListConversationsRequest)
    assert request_data.app_id == APP_ID
    assert request_data.contact_id == CONTACT_ID
    assert request_data.only_active is True
    assert request_data.page_size == 5
    assert request_data.page_token == "token_abc"
    assert request_data.active_channel == "WHATSAPP"
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_create_expects_correct_request(
    mock_sinch_client_conversation, mock_conversation_response, mocker
):
    """Test that create builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_conversation_response
    spy_endpoint = mocker.spy(CreateConversationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.create(
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        active=True,
        active_channel="WHATSAPP",
        metadata_json={"key": "value"},
        correlation_id="correlation-1",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, CreateConversationRequest)
    assert request_data.app_id == APP_ID
    assert request_data.contact_id == CONTACT_ID
    assert request_data.active is True
    assert request_data.active_channel == "WHATSAPP"
    assert request_data.metadata_json == {"key": "value"}
    assert request_data.correlation_id == "correlation-1"
    assert response is mock_conversation_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_create_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_conversation_response, mocker
):
    """Test that omitted parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_conversation_response
    spy_endpoint = mocker.spy(CreateConversationEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).conversations.create(
        app_id=APP_ID, contact_id=CONTACT_ID, correlation_id=None
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert request_data.model_fields_set == {
        "app_id",
        "contact_id",
        "correlation_id",
    }
    assert request_data.correlation_id is None


def test_conversations_get_expects_correct_request(
    mock_sinch_client_conversation, mock_conversation_response, mocker
):
    """Test that get builds the request model and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_conversation_response
    spy_endpoint = mocker.spy(GetConversationEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).conversations.get(
        conversation_id=CONVERSATION_ID
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ConversationIdRequest)
    assert kwargs["request_data"].conversation_id == CONVERSATION_ID
    assert response is mock_conversation_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete builds the request model and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteConversationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.delete(conversation_id=CONVERSATION_ID)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ConversationIdRequest)
    assert kwargs["request_data"].conversation_id == CONVERSATION_ID
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_update_expects_correct_request(
    mock_sinch_client_conversation, mock_conversation_response, mocker
):
    """Test that update builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_conversation_response
    spy_endpoint = mocker.spy(UpdateConversationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.update(
        conversation_id=CONVERSATION_ID,
        active=False,
        active_channel="SMS",
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        metadata_json={"key": "value"},
        correlation_id="correlation-1",
        metadata_update_strategy="MERGE_PATCH",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, UpdateConversationRequest)
    assert request_data.conversation_id == CONVERSATION_ID
    assert request_data.active is False
    assert request_data.active_channel == "SMS"
    assert request_data.app_id == APP_ID
    assert request_data.contact_id == CONTACT_ID
    assert request_data.metadata_json == {"key": "value"}
    assert request_data.correlation_id == "correlation-1"
    assert request_data.metadata_update_strategy == "MERGE_PATCH"
    assert response is mock_conversation_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_update_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_conversation_response, mocker
):
    """Test that omitted body parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_conversation_response
    spy_endpoint = mocker.spy(UpdateConversationEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).conversations.update(
        conversation_id=CONVERSATION_ID, metadata_json=None
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert "active" not in request_data.model_fields_set
    assert "correlation_id" not in request_data.model_fields_set
    assert "metadata_json" in request_data.model_fields_set
    assert request_data.metadata_json is None


def test_conversations_list_recent_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list_recent builds the request model and returns a TokenBasedPaginator."""
    mock_response = ListRecentConversationsResponse(conversations=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListRecentConversationsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.list_recent(
        app_id=APP_ID,
        only_active=True,
        page_size=5,
        page_token="token_abc",
        order="ASC",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ListRecentConversationsRequest)
    assert request_data.app_id == APP_ID
    assert request_data.only_active is True
    assert request_data.page_size == 5
    assert request_data.page_token == "token_abc"
    assert request_data.order == "ASC"
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_stop_active_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that stop_active builds the request model and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(StopActiveConversationEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.stop_active(conversation_id=CONVERSATION_ID)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ConversationIdRequest)
    assert kwargs["request_data"].conversation_id == CONVERSATION_ID
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_inject_message_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that inject_message builds the request model from every parameter and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(InjectMessageEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.inject_message(
        conversation_id=CONVERSATION_ID,
        contact_id=CONTACT_ID,
        channel_identity={"channel": "SMS", "identity": "+46701234567"},
        direction="TO_CONTACT",
        accept_time=ACCEPT_TIME,
        app_message={"text_message": {"text": "Hello"}},
        sender_id="sender-1",
        processing_mode="CONVERSATION",
        metadata="my metadata",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, InjectMessageRequest)
    assert request_data.conversation_id == CONVERSATION_ID
    assert request_data.contact_id == CONTACT_ID
    assert request_data.channel_identity.channel == "SMS"
    assert request_data.channel_identity.identity == "+46701234567"
    assert request_data.direction == "TO_CONTACT"
    assert request_data.accept_time == ACCEPT_TIME
    assert isinstance(request_data.app_message, TextAppMessage)
    assert request_data.app_message.text_message.text == "Hello"
    assert request_data.sender_id == "sender-1"
    assert request_data.processing_mode == "CONVERSATION"
    assert request_data.metadata == "my metadata"
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_inject_message_expects_contact_message_request(
    mock_sinch_client_conversation, mocker
):
    """Test that inject_message forwards a contact message and leaves app_message unset."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(InjectMessageEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).conversations.inject_message(
        conversation_id=CONVERSATION_ID,
        contact_id=CONTACT_ID,
        channel_identity={"channel": "SMS", "identity": "+46701234567"},
        direction="TO_APP",
        accept_time=ACCEPT_TIME,
        contact_message={"text_message": {"text": "Hi"}},
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert isinstance(request_data.contact_message, TextContactMessage)
    assert "app_message" not in request_data.model_fields_set


def test_conversations_inject_message_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mocker
):
    """Test that omitted parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(InjectMessageEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).conversations.inject_message(
        conversation_id=CONVERSATION_ID,
        contact_id=CONTACT_ID,
        channel_identity={"channel": "SMS", "identity": "+46701234567"},
        direction="TO_CONTACT",
        accept_time=ACCEPT_TIME,
        app_message={"text_message": {"text": "Hello"}},
        metadata=None,
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert request_data.model_fields_set == {
        "conversation_id",
        "contact_id",
        "channel_identity",
        "direction",
        "accept_time",
        "app_message",
        "metadata",
    }
    assert request_data.metadata is None


@pytest.mark.parametrize(
    "message_kwargs",
    [
        {},
        {
            "app_message": {"text_message": {"text": "Hello"}},
            "contact_message": {"text_message": {"text": "Hello"}},
        },
    ],
)
def test_conversations_inject_message_expects_invalid_body_raises_value_error(
    mock_sinch_client_conversation, message_kwargs
):
    """Test that setting neither or both of app_message and contact_message raises ValueError."""
    with pytest.raises(ValueError):
        Conversation(mock_sinch_client_conversation).conversations.inject_message(
            conversation_id=CONVERSATION_ID,
            contact_id=CONTACT_ID,
            channel_identity={"channel": "SMS", "identity": "+46701234567"},
            direction="TO_CONTACT",
            accept_time=ACCEPT_TIME,
            **message_kwargs,
        )


def test_conversations_inject_event_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that inject_event builds the request model from every parameter and returns the response."""
    mock_response = InjectEventResponse(
        event_id="01W4FFL35P4NC4K35CONVEVENT1", accepted_time=ACCEPT_TIME
    )
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(InjectEventEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).conversations.inject_event(
        conversation_id=CONVERSATION_ID,
        app_event={"generic_event": {"payload": {"key": "value"}}},
        accept_time=ACCEPT_TIME,
        contact_id=CONTACT_ID,
        channel_identity={"channel": "RCS", "identity": "+46701234567"},
        processing_mode="CONVERSATION",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, InjectEventRequest)
    assert request_data.conversation_id == CONVERSATION_ID
    assert isinstance(request_data.app_event, GenericAppEvent)
    assert request_data.app_event.generic_event.payload == {"key": "value"}
    assert request_data.accept_time == ACCEPT_TIME
    assert request_data.contact_id == CONTACT_ID
    assert request_data.channel_identity.channel == "RCS"
    assert request_data.channel_identity.identity == "+46701234567"
    assert request_data.processing_mode == "CONVERSATION"
    assert response is mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_conversations_inject_event_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mocker
):
    """Test that omitted parameters are unset and an explicit None is kept."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = InjectEventResponse()
    spy_endpoint = mocker.spy(InjectEventEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).conversations.inject_event(
        conversation_id=CONVERSATION_ID,
        app_event={"composing_event": {}},
        accept_time=ACCEPT_TIME,
        contact_id=None,
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert request_data.model_fields_set == {
        "conversation_id",
        "app_event",
        "accept_time",
        "contact_id",
    }
    assert request_data.contact_id is None
