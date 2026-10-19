import json
from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    UpdateConversationEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.update_conversation_request import (
    UpdateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)


@pytest.fixture
def request_data():
    return UpdateConversationRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        metadata_update_strategy="MERGE_PATCH",
        active=True,
        active_channel="WHATSAPP",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
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
    return UpdateConversationEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the conversation ID path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/conversations/01W4FFL35P4NC4K35CONVERS001"
    )


def test_build_query_params_expects_metadata_update_strategy(endpoint):
    """Test that metadata_update_strategy is sent as a query param."""
    query_params = endpoint.build_query_params()

    assert query_params["metadata_update_strategy"] == "MERGE_PATCH"


def test_build_query_params_expects_update_mask_from_body_fields(endpoint):
    """Test that update_mask is derived from the set body fields."""
    mask = endpoint.build_query_params()["update_mask"].split(",")

    assert set(mask) == {
        "active",
        "active_channel",
        "app_id",
        "contact_id",
        "metadata",
        "metadata_json",
        "correlation_id",
    }


def test_build_query_params_expects_empty_when_no_body_fields():
    """Test that no query params are sent when only conversation_id is set."""
    endpoint = UpdateConversationEndpoint(
        "test_project_id",
        UpdateConversationRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            metadata_update_strategy=None,
        ),
    )

    assert endpoint.build_query_params() == {}


def test_build_query_params_accepts_none_fields():
    """Test that an explicit None is listed in update_mask."""
    endpoint = UpdateConversationEndpoint(
        "test_project_id",
        UpdateConversationRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            active=False,
            metadata_json=None,
        ),
    )

    mask = endpoint.build_query_params()["update_mask"].split(",")

    assert set(mask) == {"active", "metadata_json"}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that path and query params are excluded from the body."""
    body = json.loads(endpoint.request_body())

    assert body == {
        "active": True,
        "active_channel": "WHATSAPP",
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "contact_id": "01W4FFL35P4NC4K35CONTACT001",
        "metadata": "legacy metadata",
        "metadata_json": {"key": "value"},
        "correlation_id": "correlation-1",
    }


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and omitted fields are absent."""
    endpoint = UpdateConversationEndpoint(
        "test_project_id",
        UpdateConversationRequest(
            conversation_id="01W4FFL35P4NC4K35CONVERS001",
            active=False,
            metadata_json=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["active"] is False
    assert body["metadata_json"] is None
    assert "correlation_id" not in body
    assert "app_id" not in body


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
