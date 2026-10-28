import json
from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    CreateConversationEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.create_conversation_request import (
    CreateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)


@pytest.fixture
def request_data():
    return CreateConversationRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        active=True,
        active_channel="WHATSAPP",
        metadata="legacy metadata",
        metadata_json={"key": "value"},
        correlation_id="correlation-1",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35CONVERS001",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            "contact_id": "01W4FFL35P4NC4K35CONTACT001",
            "active": True,
            "active_channel": "WHATSAPP",
            "metadata": "legacy metadata",
            "metadata_json": {"key": "value"},
            "correlation_id": "correlation-1",
            "last_received": "2026-10-09T10:00:00Z",
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
    return CreateConversationEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly (no path params beyond project_id)."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations"
    )


def test_build_query_params_expects_no_query_params(endpoint):
    """Test that the create request sends no query params."""
    assert endpoint.build_query_params() == {}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that every field is serialized into the body and path params are excluded."""
    body = json.loads(endpoint.request_body())

    assert body == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "active": True,
        "active_channel": "WHATSAPP",
        "metadata": "legacy metadata",
        "metadata_json": {"key": "value"},
        "correlation_id": "correlation-1",
    }
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and omitted fields are absent."""
    endpoint = CreateConversationEndpoint(
        "test_project_id",
        CreateConversationRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            correlation_id=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert body["correlation_id"] is None
    assert "metadata_json" not in body
    assert "active" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ConversationResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ConversationResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35CONVERS001"
    assert parsed_response.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert parsed_response.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert parsed_response.active is True
    assert parsed_response.active_channel == "WHATSAPP"
    assert parsed_response.metadata == "legacy metadata"
    assert parsed_response.metadata_json == {"key": "value"}
    assert parsed_response.correlation_id == "correlation-1"
    assert parsed_response.last_received == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )
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
