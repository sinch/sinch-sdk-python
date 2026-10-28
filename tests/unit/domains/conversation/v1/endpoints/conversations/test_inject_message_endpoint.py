import json
from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    InjectMessageEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_message_request import (
    InjectMessageRequest,
)

ACCEPT_TIME = datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def request_data():
    return InjectMessageRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identity={
            "channel": "MESSENGER",
            "identity": "7968425018576406",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        },
        direction="TO_CONTACT",
        accept_time=ACCEPT_TIME,
        app_message={"text_message": {"text": "Injected text message"}},
        sender_id="sender-1",
        processing_mode="CONVERSATION",
        metadata="my metadata",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={},
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
    return InjectMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the :inject-message custom verb."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations/01W4FFL35P4NC4K35CONVERS001:inject-message"
    )


def test_request_body_expects_correct_body(endpoint):
    """Test that the body carries every field except the path params."""
    body = json.loads(endpoint.request_body())

    assert body == {
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "channel_identity": {
            "channel": "MESSENGER",
            "identity": "7968425018576406",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        },
        "direction": "TO_CONTACT",
        "accept_time": "2026-10-09T10:00:00Z",
        "app_message": {"text_message": {"text": "Injected text message"}},
        "sender_id": "sender-1",
        "processing_mode": "CONVERSATION",
        "metadata": "my metadata",
    }
    assert "conversation_id" not in body
    assert "project_id" not in body


def test_request_body_expects_contact_message_serialized():
    """Test that a contact message is serialized under contact_message."""
    endpoint = InjectMessageEndpoint(
        "test_project_id",
        InjectMessageRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            channel_identity={"channel": "SMS", "identity": "+46701234567"},
            direction="TO_APP",
            accept_time=ACCEPT_TIME,
            contact_message={
                "choice_response_message": {
                    "message_id": "01W4FFL35P4NC4K35MESSAGE001",
                    "postback_data": "postback",
                },
                "reply_to": {"message_id": "01W4FFL35P4NC4K35MESSAGE001"},
            },
        ),
    )

    body = json.loads(endpoint.request_body())

    assert body["contact_message"] == {
        "choice_response_message": {
            "message_id": "01W4FFL35P4NC4K35MESSAGE001",
            "postback_data": "postback",
        },
        "reply_to": {"message_id": "01W4FFL35P4NC4K35MESSAGE001"},
    }
    assert "app_message" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = InjectMessageEndpoint(
        "test_project_id",
        InjectMessageRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            channel_identity={"channel": "SMS", "identity": "+46701234567"},
            direction="TO_CONTACT",
            accept_time=ACCEPT_TIME,
            app_message={"text_message": {"text": "Hello"}},
            metadata=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["app_message"] == {"text_message": {"text": "Hello"}}
    assert body["metadata"] is None
    assert "sender_id" not in body
    assert "processing_mode" not in body


def test_handle_response_expects_no_return_model(endpoint, mock_response):
    """Test that a successful injection does not return a response model."""
    assert endpoint.handle_response(mock_response) is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
