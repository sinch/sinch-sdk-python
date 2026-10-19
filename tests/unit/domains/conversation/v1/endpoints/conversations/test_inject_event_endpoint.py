import json
from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    InjectEventEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_event_request import (
    InjectEventRequest,
)
from sinch.domains.conversation.models.v1.conversations.response.inject_event_response import (
    InjectEventResponse,
)

ACCEPT_TIME = datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def request_data():
    return InjectEventRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        app_event={"generic_event": {"payload": {"key": "value"}}},
        accept_time=ACCEPT_TIME,
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identity={"channel": "RCS", "identity": "+46701234567"},
        processing_mode="CONVERSATION",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "event_id": "01W4FFL35P4NC4K35CONVEVENT1",
            "accepted_time": "2026-10-09T10:00:00Z",
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
    return InjectEventEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the :inject-event custom verb."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations/01W4FFL35P4NC4K35CONVERS001:inject-event"
    )


def test_request_body_expects_correct_body(endpoint):
    """Test that the body carries every field except the path params."""
    body = json.loads(endpoint.request_body())

    assert body == {
        "app_event": {"generic_event": {"payload": {"key": "value"}}},
        "accept_time": "2026-10-09T10:00:00Z",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "channel_identity": {"channel": "RCS", "identity": "+46701234567"},
        "processing_mode": "CONVERSATION",
    }
    assert "conversation_id" not in body
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = InjectEventEndpoint(
        "test_project_id",
        InjectEventRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            app_event={"composing_event": {}},
            accept_time=ACCEPT_TIME,
            contact_id=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["app_event"] == {"composing_event": {}}
    assert body["contact_id"] is None
    assert "channel_identity" not in body
    assert "processing_mode" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into an InjectEventResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, InjectEventResponse)
    assert parsed_response.event_id == "01W4FFL35P4NC4K35CONVEVENT1"
    assert parsed_response.accepted_time == ACCEPT_TIME
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
