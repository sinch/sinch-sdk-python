import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.transcoding_endpoints import (
    TranscodeMessageEndpoint,
)
from sinch.domains.conversation.models.v1.transcoding.internal.transcode_message_request import (
    TranscodeMessageRequest,
)
from sinch.domains.conversation.models.v1.transcoding.response.transcode_message_response import (
    TranscodeMessageResponse,
)

APP_MESSAGE = {
    "location_message": {
        "title": "Phare d'Eckmühl",
        "coordinates": {"latitude": 47.5, "longitude": -4.5},
    }
}


@pytest.fixture
def request_data():
    return TranscodeMessageRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        app_message=APP_MESSAGE,
        channels=["SMS", "WHATSAPP"],
        from_="sender",
        to="recipient",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "transcoded_message": {"SMS": "text", "WHATSAPP": "{}"},
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
    return TranscodeMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/messages:transcode"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that every field is serialized with its wire name, including the ``from`` alias."""
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert (
        body["app_message"]["location_message"]["title"] == "Phare d'Eckmühl"
    )
    assert body["channels"] == ["SMS", "WHATSAPP"]
    assert body["from"] == "sender"
    assert body["to"] == "recipient"
    assert "from_" not in body
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = TranscodeMessageEndpoint(
        "test_project_id",
        TranscodeMessageRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            app_message=APP_MESSAGE,
            channels=["SMS"],
            to=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["to"] is None
    assert "from" not in body

    unset_endpoint = TranscodeMessageEndpoint(
        "test_project_id",
        TranscodeMessageRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            app_message=APP_MESSAGE,
            channels=["SMS"],
        ),
    )
    unset_body = json.loads(unset_endpoint.request_body())
    assert "to" not in unset_body
    assert "from" not in unset_body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a TranscodeMessageResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, TranscodeMessageResponse)
    assert parsed_response.transcoded_message == {
        "SMS": "text",
        "WHATSAPP": "{}",
    }


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that an error response raises a ConversationException."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert "Invalid argument" in str(exc_info.value)
