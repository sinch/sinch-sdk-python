import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.event_destinations_endpoints import (
    ListEventDestinationsEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.list_event_destinations_response import (
    ListEventDestinationsResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)


@pytest.fixture
def request_data():
    return AppIdRequest(app_id="01W4FFL35P4NC4K35CONVAPP001")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "webhooks": [
                {
                    "id": "01W4FFL35P4NC4K35WEBHOOK001",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                    "target": "https://my-server.com/events",
                    "target_type": "HTTP",
                    "secret": "my-secret",
                    "triggers": ["CAPABILITY", "OPT_IN"],
                    "client_credentials": {
                        "endpoint": "https://my-auth-server.com/oauth2/token",
                        "client_id": "my-client-id",
                        "client_secret": "my-client-secret",
                        "scope": "read",
                        "response_type": "token",
                        "token_request_type": "FORM",
                    },
                    "extra_field": "extra",
                },
                {
                    "id": "01W4FFL35P4NC4K35WEBHOOK002",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                    "target": "https://my-server.com/contact",
                    "target_type": "HTTP",
                    "triggers": ["CONTACT_CREATE"],
                    "client_credentials": None,
                },
            ]
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
    return ListEventDestinationsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the app ID path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01W4FFL35P4NC4K35CONVAPP001/webhooks"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a ListEventDestinationsResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListEventDestinationsResponse)
    assert len(parsed_response.content) == 2
    assert all(
        isinstance(item, EventDestinationResponse)
        for item in parsed_response.content
    )
    assert parsed_response.content[0].id == "01W4FFL35P4NC4K35WEBHOOK001"
    assert isinstance(
        parsed_response.content[0].client_credentials, ClientCredentials
    )
    assert parsed_response.content[1].triggers == ["CONTACT_CREATE"]
    assert parsed_response.content[1].client_credentials is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
