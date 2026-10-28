import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.events_endpoints import (
    SendEventEndpoint,
)
from sinch.domains.conversation.models.v1.events.internal.send_event_request import (
    SendEventRequest,
)
from sinch.domains.conversation.models.v1.events.response.send_event_response import (
    SendEventResponse,
)


@pytest.fixture
def request_data():
    return SendEventRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        event={"composing_event": {}},
        callback_url="https://my-server.com/events",
        channel_priority_order=["WHATSAPP"],
        event_metadata="metadata",
        queue="HIGH_PRIORITY",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "event_id": "01W4FFL35P4NC4K35EVENT0001",
            "accepted_time": "2026-10-09T10:00:00Z",
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
    return SendEventEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/events:send"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that every field is serialized with its wire name."""
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert body["recipient"] == {"contact_id": "01W4FFL35P4NC4K35CONTACT001"}
    assert body["event"] == {"composing_event": {}}
    assert body["callback_url"] == "https://my-server.com/events"
    assert body["channel_priority_order"] == ["WHATSAPP"]
    assert body["event_metadata"] == "metadata"
    assert body["queue"] == "HIGH_PRIORITY"
    assert "project_id" not in body


def test_request_body_expects_identified_by_recipient():
    """Test that a channel identities recipient is serialized under identified_by."""
    endpoint = SendEventEndpoint(
        "test_project_id",
        SendEventRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            recipient={
                "identified_by": {
                    "channel_identities": [
                        {"channel": "SMS", "identity": "46700000000"}
                    ]
                }
            },
            event={"generic_event": {"payload": {"key": "value"}}},
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["recipient"] == {
        "identified_by": {
            "channel_identities": [
                {"channel": "SMS", "identity": "46700000000"}
            ]
        }
    }
    assert body["event"] == {"generic_event": {"payload": {"key": "value"}}}


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = SendEventEndpoint(
        "test_project_id",
        SendEventRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
            event={"composing_event": {}},
            event_metadata=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["event_metadata"] is None
    assert "queue" not in body
    assert "callback_url" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a SendEventResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, SendEventResponse)
    assert parsed_response.event_id == "01W4FFL35P4NC4K35EVENT0001"
    assert parsed_response.accepted_time.year == 2026


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
