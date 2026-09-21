import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    ListAppsEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_request import (
    ListAppsRequest,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_response import (
    ListAppsResponse,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_custom_response import (
    ListAppsCustomResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import StaticBearerChannelCredentials, StaticTokenChannelCredentials
from sinch.domains.conversation.models.v1.credentials.shared.static_bearer_credentials import StaticBearerCredentials
from sinch.domains.conversation.models.v1.credentials.shared.static_token_credentials import StaticTokenCredentials


@pytest.fixture
def request_data():
    return ListAppsRequest()


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "apps": [
                {
                    "id": "app-1",
                    "display_name": "First",
                    "channel_credentials": [
                        {
                            "channel": "SMS",
                            "static_bearer": {"token": "sms-token", "claimed_identity": "sp-id"},
                            "callback_secret": "sms-secret",
                            "state": {"status": "ACTIVE"},
                            "channel_known_id": "sms-known-id",
                        }
                    ],
                },
                {
                    "id": "app-2",
                    "display_name": "Second",
                    "channel_credentials": [
                        {
                            "channel": "MESSENGER",
                            "static_token": {"token": "fb-token-2"},
                        }
                    ],
                },
            ]
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=401,
        body={
            "error": {
                "code": 401,
                "message": "Unauthenticated",
                "status": "UNAUTHENTICATED",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListAppsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a ListAppsResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListAppsResponse)
    assert len(parsed_response.content) == 2
    assert all(isinstance(app, AppResponse) for app in parsed_response.content)
    assert parsed_response.content[0].id == "app-1"
    assert parsed_response.content[1].display_name == "Second"
    assert len(parsed_response.content[0].channel_credentials) == 1
    assert len(parsed_response.content[1].channel_credentials) == 1
    assert isinstance(parsed_response.content[0].channel_credentials[0], StaticBearerChannelCredentials)
    assert isinstance(parsed_response.content[0].channel_credentials[0].static_bearer, StaticBearerCredentials)
    assert isinstance(parsed_response.content[1].channel_credentials[0], StaticTokenChannelCredentials)
    assert isinstance(parsed_response.content[1].channel_credentials[0].static_token, StaticTokenCredentials)


def test_handle_response_expects_correct_mapping_with_custom_response(request_data, mock_response):
    """Test that the response is parsed and mapped into a ListAppsCustomResponse correctly."""
    parsed_response = ListAppsEndpoint("test_project_id", request_data, ListAppsCustomResponse).handle_response(mock_response)

    assert isinstance(parsed_response, ListAppsCustomResponse)
    assert len(parsed_response.content) == 2
    assert all(isinstance(app, AppResponse) for app in parsed_response.content)
    assert parsed_response.content[0].id == "app-1"
    assert parsed_response.content[1].display_name == "Second"
    assert isinstance(parsed_response.content[0].channel_credentials.sms, StaticBearerCredentials)
    assert isinstance(parsed_response.content[1].channel_credentials.messenger, StaticTokenCredentials)
    

def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 401
