import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    CreateContactEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal import (
    CreateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import ChannelIdentity


@pytest.fixture
def request_data():
    return CreateContactRequest(
        channel_identities=[{"channel": "SMS", "identity": "+12015555555"}],
        language="EN_US",
        channel_priority=["SMS"],
        display_name="Marty McFly",
        email="time.traveler@delorean.com",
        external_id="external-1",
        metadata="Some metadata",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35CONTACT001",
            "channel_identities": [
                {"channel": "SMS", "identity": "12015555555", "app_id": ""}
            ],
            "channel_priority": ["SMS"],
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
    return CreateContactEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly for the contacts collection."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that every provided field is serialized into the body."""
    body = json.loads(endpoint.request_body())

    assert body["channel_identities"] == [
        {"channel": "SMS", "identity": "+12015555555"}
    ]
    assert body["language"] == "EN_US"
    assert body["channel_priority"] == ["SMS"]
    assert body["display_name"] == "Marty McFly"
    assert body["email"] == "time.traveler@delorean.com"
    assert body["external_id"] == "external-1"
    assert body["metadata"] == "Some metadata"
    assert "project_id" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and omitted fields are absent."""
    endpoint = CreateContactEndpoint(
        "test_project_id",
        CreateContactRequest(
            channel_identities=[
                {"channel": "SMS", "identity": "+12015555555"}
            ],
            language="EN_US",
            display_name="Marty McFly",
            email=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["display_name"] == "Marty McFly"
    assert body["email"] is None
    assert "metadata" not in body
    assert "external_id" not in body
    assert "channel_priority" not in body


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
    assert parsed_response.channel_priority == ["SMS"]
    assert parsed_response.channel_identities[0] == ChannelIdentity(
        channel="SMS", identity="12015555555", app_id="")


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
