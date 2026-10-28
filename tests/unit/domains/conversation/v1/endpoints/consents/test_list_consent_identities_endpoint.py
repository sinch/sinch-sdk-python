import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.consents_endpoints import (
    ListConsentIdentitiesEndpoint,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_request import (
    ListConsentIdentitiesRequest,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_response import (
    ListConsentIdentitiesResponse,
)
from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)


@pytest.fixture
def request_data():
    return ListConsentIdentitiesRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        list_type="OPT_OUT_ALL",
        page_size=5,
        page_token="token_abc",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "identities": [
                {"identity": "33612345678"},
                {"identity": "33687654321"},
            ],
            "next_page_token": "token_next_page_abc",
            "unexpected_field": "kept",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "code": 404,
                "message": "information not found",
                "status": "NOT_FOUND",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListConsentIdentitiesEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL contains the app ID and the list type."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01W4FFL35P4NC4K35CONVAPP001/consents/OPT_OUT_ALL"
    )


def test_build_query_params_expects_parsed_params(endpoint):
    """Test that only the pagination fields are serialized as query params."""
    assert endpoint.build_query_params() == {
        "page_size": 5,
        "page_token": "token_abc",
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that fields passed as None are excluded from the query params."""
    endpoint = ListConsentIdentitiesEndpoint(
        "test_project_id",
        ListConsentIdentitiesRequest(
            app_id="APP123", list_type="OPT_OUT_MARKETING", page_size=None
        ),
    )

    assert endpoint.build_query_params() == {}


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ListConsentIdentitiesResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListConsentIdentitiesResponse)
    assert len(parsed_response.content) == 2
    assert isinstance(parsed_response.content[0], ConsentIdentityResponse)
    assert parsed_response.content[0].identity == "33612345678"
    assert parsed_response.content[1].identity == "33687654321"
    assert parsed_response.next_page_token == "token_next_page_abc"
    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "information not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
