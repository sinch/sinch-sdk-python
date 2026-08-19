"""
Unit tests for Conversation Contacts API
"""
import pytest

from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1.contacts_apis import Contacts
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    CreateContactEndpoint,
    DeleteContactEndpoint,
    GetContactEndpoint,
    ListContactsEndpoint,
    UpdateContactEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_response import (
    ListContactsResponse,
)
from sinch.domains.conversation.models.v1.contacts.internal import (
    ContactIdRequest,
    CreateContactRequest,
    ListContactsRequest,
    UpdateContactRequest,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.channel_identity import ChannelIdentity


@pytest.fixture
def mock_contact_response():
    return ContactResponse(
        id="01W4FFL35P4NC4K35CONTACT001",
        display_name="Marty McFly",
    )


def test_conversation_expects_contacts_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .contacts as a Contacts instance."""
    conversation = Conversation(mock_sinch_client_conversation)
    assert isinstance(conversation.contacts, Contacts)


def test_contacts_create_expects_correct_request(
    mock_sinch_client_conversation, mock_contact_response, mocker
):
    """Test that create sends the correct request with all parameters and returns ContactResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_contact_response
    )
    spy_endpoint = mocker.spy(CreateContactEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.contacts.create(
        channel_identities=[{"channel": "SMS", "identity": "+12015555555"}],
        language="EN_US",
        channel_priority=["SMS"],
        display_name="Marty McFly",
        email="time.traveler@delorean.com",
        external_id="external-1",
        metadata="Some metadata",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, CreateContactRequest)
    assert request_data.channel_identities[0] == ChannelIdentity(
        channel="SMS", identity="+12015555555"
    )
    assert request_data.language == "EN_US"
    assert request_data.channel_priority == ["SMS"]
    assert request_data.display_name == "Marty McFly"
    assert request_data.email == "time.traveler@delorean.com"
    assert request_data.external_id == "external-1"
    assert request_data.metadata == "Some metadata"

    assert isinstance(response, ContactResponse)
    assert response.id == "01W4FFL35P4NC4K35CONTACT001"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_contacts_create_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_contact_response, mocker
):
    """Test that optional parameters left out are not included in the request as set fields."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_contact_response
    )
    spy_endpoint = mocker.spy(CreateContactEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).contacts.create(
        channel_identities=[{"channel": "SMS", "identity": "+12015555555"}],
        language="EN_US",
    )

    _, kwargs = spy_endpoint.call_args
    fields_set = kwargs["request_data"].model_fields_set

    assert "channel_identities" in fields_set
    assert "language" in fields_set
    assert "display_name" not in fields_set
    assert "email" not in fields_set
    assert "external_id" not in fields_set
    assert "metadata" not in fields_set
    assert "channel_priority" not in fields_set


def test_contacts_get_expects_correct_request(
    mock_sinch_client_conversation, mock_contact_response, mocker
):
    """Test that get sends the contact_id and returns ContactResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_contact_response
    )
    spy_endpoint = mocker.spy(GetContactEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).contacts.get(
        contact_id="01W4FFL35P4NC4K35CONTACT001"
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ContactIdRequest)
    assert (
        kwargs["request_data"].contact_id == "01W4FFL35P4NC4K35CONTACT001"
    )

    assert isinstance(response, ContactResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_contacts_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete sends the contact_id and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteContactEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).contacts.delete(
        contact_id="01W4FFL35P4NC4K35CONTACT001"
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ContactIdRequest)
    assert (
        kwargs["request_data"].contact_id == "01W4FFL35P4NC4K35CONTACT001"
    )

    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_contacts_update_expects_correct_request(
    mock_sinch_client_conversation, mock_contact_response, mocker
):
    """Test that update sends the correct request with all parameters and returns ContactResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_contact_response
    )
    spy_endpoint = mocker.spy(UpdateContactEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).contacts.update(
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

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, UpdateContactRequest)
    assert request_data.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert request_data.channel_identities[0] == ChannelIdentity(
        channel="MESSENGER",
        identity="7968425018576406",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
    )
    assert request_data.channel_priority[0] == "MESSENGER"
    assert request_data.display_name == "Marty McFly"
    assert request_data.email == "time.traveler@delorean.com"
    assert request_data.external_id == "external-1"
    assert request_data.language == "FR"
    assert request_data.metadata == "Some metadata"

    assert isinstance(response, ContactResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_contacts_update_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_contact_response, mocker
):
    """Test that an explicit None is kept while omitted parameters stay unset."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_contact_response
    )
    spy_endpoint = mocker.spy(UpdateContactEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).contacts.update(
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        display_name="Marty McFly",
        email=None,
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    fields_set = request_data.model_fields_set

    assert request_data.display_name == "Marty McFly"
    assert "email" in fields_set
    assert request_data.email is None
    assert "metadata" not in fields_set
    assert "channel_identities" not in fields_set


def test_contacts_list_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list sends the correct request and returns a TokenBasedPaginator."""
    mock_response = ListContactsResponse(contacts=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_response
    )
    spy_endpoint = mocker.spy(ListContactsEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).contacts.list(
        page_size=10,
        page_token="a-token",
        external_id="external-1",
        channel="SMS",
        identity="+12015555555",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ListContactsRequest)
    assert request_data.page_size == 10
    assert request_data.page_token == "a-token"
    assert request_data.external_id == "external-1"
    assert request_data.channel == "SMS"
    assert request_data.identity == "+12015555555"

    assert isinstance(response, TokenBasedPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
