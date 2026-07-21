import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    UpdateAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.request.update_app_request import (
    UpdateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.static_bearer_credentials import StaticBearerCredentials


@pytest.fixture
def request_data():
    return UpdateAppRequest(
        app_id="01FC66621XXXXX119Z8PMV1QPQ",
        channel_credentials={
            "SMS": {"token": "my-token", "claimed_identity": "identity"}
        },
        display_name="Updated App",
        smart_conversation={"enabled": True},
        event_destination_settings={
            "secret_for_overridden_callback_urls": "secret"
        },
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "display_name": "Updated App",
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
    return UpdateAppEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the app_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_build_query_params_expects_update_mask_from_body_fields(endpoint):
    """Test that update_mask is derived from the set body fields, using aliases."""
    query_params = endpoint.build_query_params()

    mask = query_params["update_mask"].split(",")
    assert "display_name" in mask
    assert "smart_conversation" in mask
    assert "callback_settings" in mask
    assert "app_id" not in mask
    assert "update_mask" not in mask
    assert "channel_credentials" in mask


def test_build_query_params_expects_empty_when_no_body_fields():
    """Test that update_mask is omitted when only app_id is set (no fields to update)."""
    endpoint = UpdateAppEndpoint(
        "test_project_id",
        UpdateAppRequest(app_id="01FC66621XXXXX119Z8PMV1QPQ"),
    )

    assert endpoint.build_query_params() == {}


def test_request_body_expects_correct_serialization(request_data):
    """Test that app_id is excluded from the body and aliases are applied."""
    endpoint = UpdateAppEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "app_id" not in body
    assert "update_mask" not in body
    assert body["display_name"] == "Updated App"
    assert body["smart_conversation"]["enabled"] is True
    assert body["callback_settings"]["secret_for_overridden_callback_urls"] == "secret"
    assert "event_destination_settings" not in body
    assert body["channel_credentials"][0]["static_bearer"]["token"] == "my-token"
    assert body["channel_credentials"][0]["static_bearer"]["claimed_identity"] == "identity"
    assert body["channel_credentials"][0]["channel"] == "SMS"


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into an AppResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, AppResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "Updated App"
    assert parsed_response.smart_conversation.enabled is True
    assert parsed_response.event_destination_settings.secret_for_overridden_target == "secret"
    assert parsed_response.channel_credentials[0].channel == "SMS"
    assert parsed_response.channel_credentials[0].static_bearer.token == "my-token"
    assert parsed_response.channel_credentials[0].static_bearer.claimed_identity == "identity"


def test_handle_response_expects_correct_mapping_with_custom_response(request_data, mock_response):
    """Test that the response is parsed and mapped into an AppCustomResponse correctly."""
    parsed_response = UpdateAppEndpoint("test_project_id", request_data, AppCustomResponse).handle_response(mock_response)

    assert isinstance(parsed_response, AppCustomResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.display_name == "Updated App"
    assert parsed_response.smart_conversation.enabled is True
    assert parsed_response.event_destination_settings.secret_for_overridden_target == "secret"
    assert isinstance(parsed_response.channel_credentials.sms, StaticBearerCredentials)
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
