import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    ListContactsEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_response import (
    ListContactsResponse,
)
from sinch.domains.conversation.models.v1.contacts.internal import (
    ListContactsRequest,
)


@pytest.fixture
def request_data():
    return ListContactsRequest(
        page_size=10,
        page_token="a-token",
        external_id="external-1",
        channel="SMS",
        identity="+12015555555",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "contacts": [
                {
                    "id": "01W4FFL35P4NC4K35CONTACT001",
                    "channel_identities": [
                        {
                            "channel": "SMS",
                            "identity": "12015555555",
                            "app_id": "",
                        }
                    ],
                    "channel_priority": [],
                    "display_name": "Marty McFly",
                    "email": "time.traveler@delorean.com",
                    "external_id": "",
                    "metadata": "",
                    "language": "EN_US",
                },
                {
                    "id": "01W4FFL35P4NC4K35CONTACT002",
                    "channel_identities": [
                        {
                            "channel": "MMS",
                            "identity": "12016666666",
                            "app_id": "",
                        }
                    ],
                    "channel_priority": ["MMS"],
                    "display_name": "Pika pika",
                    "email": "pikachu@poke.mon",
                    "external_id": "",
                    "metadata": "Some metadata",
                    "language": "EN_US",
                },
            ],
            "next_page_token": "ChowMVc0RkZMMzVQNE5DNEszNUNPTlRBQ1QwMDI=",
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
    return ListContactsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly for the contacts collection."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts"
    )


def test_build_query_params_expects_all_fields(endpoint):
    """Test that every filter is serialized into the query params."""
    assert endpoint.build_query_params() == {
        "page_size": 10,
        "page_token": "a-token",
        "external_id": "external-1",
        "channel": "SMS",
        "identity": "+12015555555",
    }


def test_build_query_params_excludes_none_fields():
    """Test that a field passed as None is excluded from the query params."""
    endpoint = ListContactsEndpoint(
        "test_project_id",
        ListContactsRequest(page_size=10, page_token=None, channel=None),
    )

    assert endpoint.build_query_params() == {"page_size": 10}


def test_request_body_expects_no_body(endpoint):
    """Test that query params never leak into the body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed into a ListContactsResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListContactsResponse)
    assert (
        parsed_response.next_page_token
        == "ChowMVc0RkZMMzVQNE5DNEszNUNPTlRBQ1QwMDI="
    )
    assert len(parsed_response.contacts) == 2
    assert parsed_response.contacts[0].id == "01W4FFL35P4NC4K35CONTACT001"
    assert parsed_response.contacts[1].display_name == "Pika pika"
    assert parsed_response.contacts[1].channel_priority == ["MMS"]


def test_handle_response_expects_content_property(endpoint, mock_response):
    """Test that content exposes the page items for the paginator."""
    parsed_response = endpoint.handle_response(mock_response)

    assert parsed_response.content == parsed_response.contacts
    assert len(parsed_response.content) == 2


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the message built from the error body."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
