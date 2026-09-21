"""
Unit tests for Conversation Apps API
"""
import pytest
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.api.v1 import Apps
from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    CreateAppEndpoint,
    DeleteAppEndpoint,
    GetAppEndpoint,
    ListAppsEndpoint,
    UpdateAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
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
from sinch.domains.conversation.models.v1.apps.request.create_app_request import (
    CreateAppRequest,
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
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import StaticBearerChannelCredentials, StaticTokenChannelCredentials


@pytest.fixture
def mock_app_response():
    return AppResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        display_name="My App",
    )


@pytest.fixture
def mock_app_custom_response():
    return AppCustomResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        display_name="My App",
    )


def test_conversation_expects_apps_attribute(mock_sinch_client_conversation):
    """Test that Conversation exposes .apps as an Apps instance."""
    conversation = Conversation(mock_sinch_client_conversation)
    assert isinstance(conversation.apps, Apps)


def test_apps_create_expects_correct_request(
    mock_sinch_client_conversation, mock_app_custom_response, mocker
):
    """Test that create sends the correct request with all parameters and returns AppCustomResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_custom_response
    )
    spy_endpoint = mocker.spy(CreateAppEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.create(
        channel_credentials={
            "SMS": {"claimed_identity": "sp-id", "token": "my-token"}
        },
        display_name="My App",
        conversation_metadata_report_view="FULL",
        retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 180,
        },
        dispatch_retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 7,
        },
        processing_mode="CONVERSATION",
        smart_conversation={"enabled": True},
        event_destination_settings={
            "secret_for_overridden_target": "secret"
        },
        message_retry_settings={"retry_duration": 300},
        delivery_report_based_fallback={
            "enabled": True,
            "delivery_report_waiting_time": 60,
        },
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, CreateAppRequest)
    assert request_data.display_name == "My App"
    assert request_data.channel_credentials[0].static_bearer.token == "my-token"
    assert (
        request_data.channel_credentials[0].static_bearer.claimed_identity
        == "sp-id"
    )
    assert isinstance(request_data.channel_credentials[0], StaticBearerChannelCredentials)
    assert request_data.channel_credentials[0].channel == "SMS"
    assert request_data.conversation_metadata_report_view == "FULL"
    assert request_data.retention_policy.retention_type == "MESSAGE_EXPIRE_POLICY"
    assert request_data.retention_policy.ttl_days == 180
    assert request_data.dispatch_retention_policy.ttl_days == 7
    assert request_data.processing_mode == "CONVERSATION"
    assert request_data.smart_conversation.enabled is True
    assert request_data.event_destination_settings.secret_for_overridden_target == "secret"
    assert request_data.message_retry_settings.retry_duration == 300
    assert request_data.delivery_report_based_fallback.enabled is True
    assert request_data.delivery_report_based_fallback.delivery_report_waiting_time == 60

    assert kwargs["response_model"] is AppCustomResponse
    assert isinstance(response, AppCustomResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()

def test_apps_create_with_raw_response_returns_app_response(
    mock_sinch_client_conversation, mock_app_response, mocker
):
    """Test that raw_response=True returns the AppResponse model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_response
    )
    spy_endpoint = mocker.spy(CreateAppEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.create(
        channel_credentials={
            "SMS": {"claimed_identity": "sp-id", "token": "my-token"}
        },
        display_name="My App",
        raw_response=True,
    )

    _, kwargs = spy_endpoint.call_args
    assert kwargs["response_model"] is AppResponse
    assert type(response) is AppResponse


def test_apps_update_expects_correct_request(
    mock_sinch_client_conversation, mock_app_custom_response, mocker
):
    """Test that update sends the correct request with all parameters and returns AppCustomResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_custom_response
    )
    spy_endpoint = mocker.spy(UpdateAppEndpoint, "__init__")

    app_id = "01FC66621XXXXX119Z8PMV1QPQ"
    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.update(
        app_id=app_id,
        channel_credentials={"MESSENGER": {"token": "my-token"}},
        display_name="Updated App",
        conversation_metadata_report_view="NONE",
        retention_policy={
            "retention_type": "CONVERSATION_EXPIRE_POLICY",
            "ttl_days": 90,
        },
        dispatch_retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 3,
        },
        processing_mode="DISPATCH",
        smart_conversation={"enabled": False},
        event_destination_settings={
            "secret_for_overridden_target": "secret"
        },
        message_retry_settings={"retry_duration": 600},
        delivery_report_based_fallback={
            "enabled": False,
            "delivery_report_waiting_time": 30,
        },
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]

    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, UpdateAppRequest)
    assert request_data.app_id == app_id
    assert isinstance(request_data.channel_credentials[0], StaticTokenChannelCredentials)
    assert request_data.channel_credentials[0].static_token.token == "my-token"
    assert request_data.channel_credentials[0].channel == "MESSENGER"
    assert request_data.display_name == "Updated App"
    assert request_data.conversation_metadata_report_view == "NONE"
    assert request_data.retention_policy.retention_type == "CONVERSATION_EXPIRE_POLICY"
    assert request_data.retention_policy.ttl_days == 90
    assert request_data.dispatch_retention_policy.ttl_days == 3
    assert request_data.processing_mode == "DISPATCH"
    assert request_data.smart_conversation.enabled is False
    assert request_data.event_destination_settings.secret_for_overridden_target == "secret"
    assert request_data.message_retry_settings.retry_duration == 600
    assert request_data.delivery_report_based_fallback.enabled is False
    assert request_data.delivery_report_based_fallback.delivery_report_waiting_time == 30

    assert kwargs["response_model"] is AppCustomResponse
    assert isinstance(response, AppCustomResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()

def test_apps_update_with_raw_response_returns_app_response(
    mock_sinch_client_conversation, mock_app_response, mocker
):
    """Test that raw_response=True returns AppResponse model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_response
    )
    spy_endpoint = mocker.spy(UpdateAppEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.update(
        app_id="01FC66621XXXXX119Z8PMV1QPQ",
        channel_credentials={
            "SMS": {"claimed_identity": "sp-id", "token": "my-token"}
        },
        raw_response=True,
    )

    _, kwargs = spy_endpoint.call_args
    assert kwargs["response_model"] is AppResponse
    assert type(response) is AppResponse
 

def test_apps_get_expects_correct_request(
    mock_sinch_client_conversation, mock_app_custom_response, mocker
):
    """Test that get sends the correct request and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_custom_response
    )
    spy_endpoint = mocker.spy(GetAppEndpoint, "__init__")

    app_id = "01FC66621XXXXX119Z8PMV1QPQ"
    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.get(app_id=app_id)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], AppIdRequest)
    assert kwargs["request_data"].app_id == app_id
    assert kwargs["response_model"] is AppCustomResponse
    assert isinstance(response, AppCustomResponse)
    assert response.id == app_id
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()

def test_apps_get_with_raw_response_returns_app_response(
    mock_sinch_client_conversation, mock_app_response, mocker
):
    """Test that raw_response=True returns AppResponse model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_app_response
    )
    spy_endpoint = mocker.spy(GetAppEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.get(
        app_id="01FC66621XXXXX119Z8PMV1QPQ", raw_response=True
    )

    _, kwargs = spy_endpoint.call_args
    assert kwargs["response_model"] is AppResponse
    assert type(response) is AppResponse


def test_apps_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete sends the correct request and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        None
    )
    spy_endpoint = mocker.spy(DeleteAppEndpoint, "__init__")

    app_id = "01FC66621XXXXX119Z8PMV1QPQ"
    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.delete(app_id=app_id)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], AppIdRequest)
    assert kwargs["request_data"].app_id == app_id
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_apps_list_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list sends the correct request and returns a TokenBasedPaginator using ListAppsCustomResponse."""
    mock_response = ListAppsCustomResponse(apps=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_response
    )
    spy_endpoint = mocker.spy(ListAppsEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.list()

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ListAppsRequest)

    assert isinstance(response, TokenBasedPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    assert kwargs["response_model"] is ListAppsCustomResponse
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_apps_list_with_raw_response_returns_list_app_response(
    mock_sinch_client_conversation, mocker
):
    """Test that raw_response=True returns TokenBasedPaginator using ListAppsResponse."""
    mock_response = ListAppsResponse(apps=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = (
        mock_response
    )
    spy_endpoint = mocker.spy(ListAppsEndpoint, "__init__")

    conversation = Conversation(mock_sinch_client_conversation)
    response = conversation.apps.list(raw_response=True)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ListAppsRequest)

    assert isinstance(response, TokenBasedPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    assert kwargs["response_model"] is ListAppsResponse
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
