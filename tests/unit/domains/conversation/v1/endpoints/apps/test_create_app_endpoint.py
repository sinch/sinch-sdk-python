import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    CreateAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.request.create_app_request import (
    CreateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials_response import StaticBearerChannelCredentialsResponse


@pytest.fixture
def request_data():
    return CreateAppRequest(
        channel_credentials={
            "SMS": {"token": "my-token", "claimed_identity": "identity"}
        },
        display_name="My App",
        smart_conversation={"enabled": True},
        event_destination_settings={
            "secret_for_overridden_target": "secret"
        },
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "display_name": "My App",
            "processing_mode": "CONVERSATION",
            "rate_limits": {"inbound": 25, "outbound": 25, "webhooks": 25},
            "queue_stats": {"outbound_size": 0, "outbound_limit": 500000},
            "smart_conversation": {"enabled": True},
            "callback_settings": {
                "secret_for_overridden_callback_urls": "secret"
            },
            "channel_credentials": [
                {
                    "channel": "SMS",
                    "static_bearer": {"token": "my-token", "claimed_identity": "identity"},
                }
            ],
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
    return CreateAppEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps"
    )


def test_request_body_expects_correct_serialization(request_data):
    """Test that all fields serialize correctly to the request body, applying aliases."""
    endpoint = CreateAppEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert body["display_name"] == "My App"
    assert body["channel_credentials"][0]["static_bearer"]["token"] == "my-token"
    assert body["channel_credentials"][0]["static_bearer"]["claimed_identity"] == "identity"
    assert body["channel_credentials"][0]["channel"] == "SMS"
    assert body["smart_conversation"]["enabled"] is True
    assert body["callback_settings"]["secret_for_overridden_callback_urls"] == "secret"
    assert "event_destination_settings" not in body
    assert "project_id" not in body


def test_request_body_excludes_none_fields(request_data):
    """Test that None fields are excluded from the serialized request body."""
    body = json.loads(CreateAppEndpoint("test_project_id", request_data).request_body())

    assert "retention_policy" not in body
    assert "message_retry_settings" not in body
    assert "processing_mode" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into an AppResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, AppResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "My App"
    assert parsed_response.processing_mode == "CONVERSATION"
    assert parsed_response.rate_limits.inbound == 25
    assert parsed_response.rate_limits.events == 25
    assert parsed_response.queue_stats.outbound_limit == 500000
    assert parsed_response.smart_conversation.enabled is True
    assert parsed_response.event_destination_settings.secret_for_overridden_target == "secret"
    assert parsed_response.channel_credentials[0].channel == "SMS"
    assert parsed_response.channel_credentials[0].static_bearer.token == "my-token"
    assert parsed_response.channel_credentials[0].static_bearer.claimed_identity == "identity"

def test_handle_response_expects_correct_mapping_with_custom_response(endpoint, mock_response):
    """Test that the response is parsed and mapped into an AppCustomResponse correctly."""
    parsed_response = CreateAppEndpoint("test_project_id", request_data, AppCustomResponse).handle_response(mock_response)

    assert isinstance(parsed_response, AppCustomResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "My App"
    assert parsed_response.processing_mode == "CONVERSATION"
    assert parsed_response.rate_limits.inbound == 25
    assert parsed_response.rate_limits.events == 25
    assert parsed_response.queue_stats.outbound_limit == 500000
    assert parsed_response.smart_conversation.enabled is True
    assert parsed_response.event_destination_settings.secret_for_overridden_target == "secret"
    assert isinstance(parsed_response.channel_credentials.sms, StaticBearerChannelCredentialsResponse)
    assert parsed_response.channel_credentials.sms.token == "my-token"
    assert parsed_response.channel_credentials.sms.claimed_identity == "identity"



def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
