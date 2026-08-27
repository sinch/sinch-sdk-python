import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    GetChannelProfileEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.get_channel_profile_request import (
    GetChannelProfileRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.get_channel_profile_response import (
    GetChannelProfileResponse,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)


@pytest.fixture
def request_data():
    return GetChannelProfileRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient=Recipient(contact_id="01W4FFL35P4NC4K35CONTACT001"),
        channel="MESSENGER",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "profile_name": "Marty McFly FB",
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
    return GetChannelProfileEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly for the getChannelProfile action."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts:getChannelProfile"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that app_id, recipient, and channel are serialized into the body."""
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert body["recipient"] == {"contact_id": "01W4FFL35P4NC4K35CONTACT001"}
    assert body["channel"] == "MESSENGER"


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a GetChannelProfileResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, GetChannelProfileResponse)
    assert parsed_response.profile_name == "Marty McFly FB"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
