import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    GetContactEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal import (
    ContactIdRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import ChannelIdentity


@pytest.fixture
def request_data():
    return ContactIdRequest(contact_id="01W4FFL35P4NC4K35CONTACT001")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35CONTACT001",
            "channel_identities": [
                {
                    "channel": "MESSENGER",
                    "identity": "7968425018576406",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                }
            ],
            "channel_priority": ["MESSENGER"],
            "display_name": "Marty McFly",
            "email": "time.traveler@delorean.com",
            "external_id": "external-1",
            "metadata": "Some metadata",
            "language": "EN_US",
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
    return GetContactEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the contact_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts/01W4FFL35P4NC4K35CONTACT001"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that no body is sent: contact_id is a path param only."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ContactResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ContactResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35CONTACT001"
    assert parsed_response.display_name == "Marty McFly"
    assert parsed_response.email == "time.traveler@delorean.com"
    assert parsed_response.external_id == "external-1"
    assert parsed_response.metadata == "Some metadata"
    assert parsed_response.language == "EN_US"
    assert parsed_response.channel_priority == ["MESSENGER"]
    assert parsed_response.channel_identities[0] == ChannelIdentity(
        channel="MESSENGER", identity="7968425018576406", app_id="01W4FFL35P4NC4K35CONVAPP001"
    )


def test_handle_response_expects_server_extra_fields_preserved(
    endpoint, mock_response
):
    """Test that an unexpected field in the response body is preserved on the model."""
    parsed_response = endpoint.handle_response(mock_response)

    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
