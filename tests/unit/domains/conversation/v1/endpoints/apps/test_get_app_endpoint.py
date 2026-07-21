import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    CreateAppEndpoint,
    GetAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    LineEnterpriseChannelCredentials,
    StaticBearerChannelCredentials,
    StaticTokenChannelCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.static_bearer_credentials import StaticBearerCredentials
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials_response import (
    LineEnterpriseJapanChannelCredentialsResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.static_token_credentials import StaticTokenCredentials


@pytest.fixture
def request_data():
    return AppIdRequest(app_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "display_name": "My App",
            "processing_mode": "CONVERSATION",
            "channel_credentials": [
                {
                    "channel": "SMS",
                    "static_bearer": {"token": "sms-token", "claimed_identity": "sp-id"},
                    "callback_secret": "sms-secret",
                    "state": {"status": "ACTIVE"},
                    "channel_known_id": "sms-known-id",
                },
                {
                    "channel": "MESSENGER",
                    "static_token": {"token": "fb-token"},
                },
                {
                    "channel": "LINE",
                    "line_enterprise_credentials": {
                        "line_japan": {"token": "line-token", "secret": "line-secret"}
                    },
                }
            ],
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
                "message": "App not found",
                "status": "NOT_FOUND",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetAppEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the app_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into an AppResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, AppResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "My App"
    assert parsed_response.processing_mode == "CONVERSATION"
    assert len(parsed_response.channel_credentials) == 3
    assert isinstance(parsed_response.channel_credentials[0], StaticBearerChannelCredentials)
    assert isinstance(parsed_response.channel_credentials[0].static_bearer, StaticBearerCredentials)
    assert isinstance(parsed_response.channel_credentials[1], StaticTokenChannelCredentials)
    assert isinstance(parsed_response.channel_credentials[1].static_token, StaticTokenCredentials)
    assert isinstance(parsed_response.channel_credentials[2], LineEnterpriseChannelCredentials)
    assert isinstance(parsed_response.channel_credentials[2].line_enterprise_credentials, LineEnterpriseCredentialsJapan)


def test_handle_response_expects_correct_mapping_with_custom_response(endpoint, mock_response):
    """Test that the response is parsed and mapped into an AppCustomResponse correctly."""
    parsed_response = GetAppEndpoint("test_project_id", request_data, AppCustomResponse).handle_response(mock_response)

    assert isinstance(parsed_response, AppCustomResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "My App"
    assert parsed_response.processing_mode == "CONVERSATION"
    assert isinstance(parsed_response.channel_credentials.sms, StaticBearerCredentials)
    assert isinstance(parsed_response.channel_credentials.messenger, StaticTokenCredentials)
    assert isinstance(
        parsed_response.channel_credentials.line_japan,
        LineEnterpriseJapanChannelCredentialsResponse,
    )


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
