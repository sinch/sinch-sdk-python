import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.contacts_endpoints import (
    ListIdentityConflictsEndpoint,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_request import (
    ListIdentityConflictsRequest,
)
from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_response import (
    ListIdentityConflictsResponse,
)


@pytest.fixture
def request_data():
    return ListIdentityConflictsRequest(
        page_size=10,
        page_token="a-token",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "conflicts": [
                {
                    "identity": "12015555555",
                    "channels": ["RCS", "SMS"],
                    "contact_ids": [
                        "01W4FFL35P4NC4K35CONTACT001",
                        "01W4FFL35P4NC4K35CONTACT002",
                    ],
                },
                {
                    "identity": "12016666666",
                    "channels": ["MMS", "RCS", "SMS"],
                    "contact_ids": [
                        "01W4FFL35P4NC4K35CONTACT003",
                        "01W4FFL35P4NC4K35CONTACT004",
                    ],
                },
            ],
            "next_page_token": "MTIwMTY2NjY2NjY="
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
    return ListIdentityConflictsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly for the identityConflicts collection."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/contacts:identityConflicts"
    )


def test_build_query_params_expects_all_fields(endpoint):
    """Test that page_size and page_token are serialized into the query params."""
    assert endpoint.build_query_params() == {
        "page_size": 10,
        "page_token": "a-token",
    }


def test_build_query_params_excludes_none_fields():
    """Test that a field passed as None is excluded from the query params."""
    endpoint = ListIdentityConflictsEndpoint(
        "test_project_id",
        ListIdentityConflictsRequest(page_size=10, page_token=None),
    )

    assert endpoint.build_query_params() == {"page_size": 10}


def test_request_body_expects_no_body(endpoint):
    """Test that query params never leak into the body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed into a ListIdentityConflictsResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListIdentityConflictsResponse)
    assert parsed_response.next_page_token == "MTIwMTY2NjY2NjY="
    assert len(parsed_response.conflicts) == 2
    assert parsed_response.conflicts[0].identity == "12015555555"
    assert parsed_response.conflicts[0].channels == ["RCS", "SMS"]
    assert parsed_response.conflicts[1].contact_ids == [
        "01W4FFL35P4NC4K35CONTACT003",
        "01W4FFL35P4NC4K35CONTACT004",
    ]


def test_handle_response_expects_content_property(endpoint, mock_response):
    """Test that content exposes the page items for the paginator."""
    parsed_response = endpoint.handle_response(mock_response)

    assert parsed_response.content == parsed_response.conflicts
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
