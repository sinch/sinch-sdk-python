import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    UpdateContactEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal import (
    UpdateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import ChannelIdentity


@pytest.fixture
def request_data():
    return UpdateContactRequest(
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identities=[
            {
                "channel": "MESSENGER",
                "identity": "7968425018576406",
                "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            }
        ],
        channel_priority=["MESSENGER"],
        display_name="Marty McFly",
        email="time.traveler@delorean.com",
        external_id="external-1",
        language="FR",
        metadata="Some metadata",
    )


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
            "language": "FR",
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
    return UpdateContactEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the contact_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts/01W4FFL35P4NC4K35CONTACT001"
    )


def test_build_query_params_expects_update_mask_from_body_fields(endpoint):
    """Test that update_mask is derived from the set body fields."""
    mask = endpoint.build_query_params()["update_mask"].split(",")

    assert set(mask) == {
        "channel_identities",
        "channel_priority",
        "display_name",
        "email",
        "external_id",
        "language",
        "metadata",
    }
    assert "contact_id" not in mask
    assert "update_mask" not in mask


def test_build_query_params_expects_empty_when_no_body_fields():
    """Test that update_mask is omitted when only contact_id is set."""
    endpoint = UpdateContactEndpoint(
        "test_project_id",
        UpdateContactRequest(contact_id="01W4FFL35P4NC4K35CONTACT001"),
    )

    assert endpoint.build_query_params() == {}


def test_build_query_params_accepts_none_fields():
    """Test that an explicit None is listed in update_mask."""
    endpoint = UpdateContactEndpoint(
        "test_project_id",
        UpdateContactRequest(
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            display_name="Marty McFly",
            email=None,
        ),
    )

    mask = endpoint.build_query_params()["update_mask"].split(",")

    assert set(mask) == {"display_name", "email"}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that contact_id and update_mask are excluded from the body."""
    body = json.loads(endpoint.request_body())

    assert "contact_id" not in body
    assert "update_mask" not in body
    assert "project_id" not in body
    assert body["channel_identities"] == [
        {
            "channel": "MESSENGER",
            "identity": "7968425018576406",
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        }
    ]
    assert body["channel_priority"] == ["MESSENGER"]
    assert body["display_name"] == "Marty McFly"
    assert body["email"] == "time.traveler@delorean.com"
    assert body["external_id"] == "external-1"
    assert body["language"] == "FR"
    assert body["metadata"] == "Some metadata"


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and omitted fields are absent."""
    endpoint = UpdateContactEndpoint(
        "test_project_id",
        UpdateContactRequest(
            contact_id="01W4FFL35P4NC4K35CONTACT001",
            display_name="Marty McFly",
            email=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["display_name"] == "Marty McFly"
    assert body["email"] is None
    assert "metadata" not in body
    assert "channel_identities" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ContactResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ContactResponse)
    assert parsed_response.id == "01W4FFL35P4NC4K35CONTACT001"
    assert parsed_response.display_name == "Marty McFly"
    assert parsed_response.language == "FR"
    assert parsed_response.channel_priority == ["MESSENGER"]
    assert parsed_response.channel_identities[0] == ChannelIdentity(
        channel="MESSENGER", identity="7968425018576406", app_id="01W4FFL35P4NC4K35CONVAPP001"
    )


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
