import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    MergeContactEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.merge_contact_request import (
    MergeContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)


@pytest.fixture
def request_data():
    return MergeContactRequest(
        destination_id="01W4FFL35P4NC4K35CONTACT002",
        source_id="01W4FFL35P4NC4K35CONTACT001",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01W4FFL35P4NC4K35CONTACT002",
            "channel_identities": [
                {
                    "channel": "MESSENGER",
                    "identity": "7968425018576406",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                }
            ],
            "channel_priority": ["MESSENGER"],
            "display_name": "Pika pika",
            "email": "pikachu@poke.mon",
            "external_id": "",
            "metadata": "",
            "language": "EN_US",
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
    return MergeContactEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the destination_id path param and :merge suffix."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts/01W4FFL35P4NC4K35CONTACT002:merge"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that destination_id is excluded from the body while source_id is sent."""
    body = json.loads(endpoint.request_body())

    assert "destination_id" not in body
    assert "project_id" not in body
    assert body["source_id"] == "01W4FFL35P4NC4K35CONTACT001"
    assert "strategy" not in body


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and omitted fields are absent."""
    endpoint = MergeContactEndpoint(
        "test_project_id",
        MergeContactRequest(
            destination_id="01W4FFL35P4NC4K35CONTACT002",
            source_id="01W4FFL35P4NC4K35CONTACT001",
            strategy=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["source_id"] == "01W4FFL35P4NC4K35CONTACT001"
    assert body["strategy"] is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ContactResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ContactResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35CONTACT002"
    assert parsed_response.display_name == "Pika pika"
    assert parsed_response.channel_priority == ["MESSENGER"]


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
