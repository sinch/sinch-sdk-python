"""
Unit tests for Conversation Transcoding API
"""

import pytest

from sinch.domains.conversation.api.v1 import Transcoding
from sinch.domains.conversation.api.v1.internal.transcoding_endpoints import (
    TranscodeMessageEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.transcoding.internal.transcode_message_request import (
    TranscodeMessageRequest,
)
from sinch.domains.conversation.models.v1.transcoding.response.transcode_message_response import (
    TranscodeMessageResponse,
)

APP_ID = "01W4FFL35P4NC4K35CONVAPP001"
APP_MESSAGE = {
    "location_message": {
        "title": "Phare d'Eckmühl",
        "label": "Pointe de Penmarch",
        "coordinates": {"latitude": 47.79, "longitude": -4.37},
    }
}


@pytest.fixture
def mock_transcode_message_response():
    return TranscodeMessageResponse(
        transcoded_message={"SMS": "text", "WHATSAPP": "{}"}
    )


def test_conversation_expects_transcoding_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .transcoding as a Transcoding instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.transcoding, Transcoding)


def test_transcoding_transcode_message_expects_correct_request(
    mock_sinch_client_conversation, mock_transcode_message_response, mocker
):
    """Test that transcode_message builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_transcode_message_response
    spy_endpoint = mocker.spy(TranscodeMessageEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).transcoding.transcode_message(
        app_id=APP_ID,
        app_message=APP_MESSAGE,
        channels=["SMS", "WHATSAPP"],
        from_="sender",
        to="recipient",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, TranscodeMessageRequest)
    assert request_data.app_id == APP_ID
    assert request_data.app_message.location_message.title == "Phare d'Eckmühl"
    assert request_data.channels == ["SMS", "WHATSAPP"]
    assert request_data.from_ == "sender"
    assert request_data.to == "recipient"
    assert isinstance(response, TranscodeMessageResponse)
    assert response.transcoded_message["SMS"] == "text"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_transcoding_transcode_message_expects_unset_optionals_omitted(
    mock_sinch_client_conversation, mock_transcode_message_response, mocker
):
    """Test that optional parameters left unset are not part of the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_transcode_message_response
    spy_endpoint = mocker.spy(TranscodeMessageEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).transcoding.transcode_message(
        app_id=APP_ID, app_message=APP_MESSAGE, channels=["SMS"]
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert "from_" not in request_data.model_fields_set
    assert "to" not in request_data.model_fields_set
