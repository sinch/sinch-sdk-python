"""
Unit tests for Conversation Project Settings API
"""

from sinch.core.sentinel import UNSET
from sinch.domains.conversation.api.v1 import ProjectSettings
from sinch.domains.conversation.api.v1.internal.project_settings_endpoints import (
    CreateProjectSettingsEndpoint,
    DeleteProjectSettingsEndpoint,
    GetProjectSettingsEndpoint,
    UpdateProjectSettingsEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.project_settings.internal.delete_project_settings_request import (
    DeleteProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.internal.get_project_settings_request import (
    GetProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.internal.project_settings_request import (
    ProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.response.project_settings_response import (
    ProjectSettingsResponse,
)


def test_conversation_expects_project_settings_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .project_settings as a ProjectSettings instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.project_settings, ProjectSettings)


def test_project_settings_create_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that create builds the request model and returns ProjectSettingsResponse."""
    mock_response = ProjectSettingsResponse(project_id="test_project_id")
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(CreateProjectSettingsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).project_settings.create(
        contact_settings={"unified_contact_id_enabled": True}
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ProjectSettingsRequest)
    assert request_data.contact_settings.unified_contact_id_enabled is True
    assert isinstance(response, ProjectSettingsResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_project_settings_create_expects_unset_contact_settings_omitted(
    mock_sinch_client_conversation, mocker
):
    """Test that an omitted contact_settings is not set on the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = ProjectSettingsResponse()
    spy_endpoint = mocker.spy(CreateProjectSettingsEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).project_settings.create()

    _, kwargs = spy_endpoint.call_args
    assert "contact_settings" not in kwargs["request_data"].model_fields_set


def test_project_settings_get_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that get builds the empty request model and returns ProjectSettingsResponse."""
    mock_response = ProjectSettingsResponse(project_id="test_project_id")
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(GetProjectSettingsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).project_settings.get()

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], GetProjectSettingsRequest)
    assert isinstance(response, ProjectSettingsResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_project_settings_update_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that update builds the request model and returns ProjectSettingsResponse."""
    mock_response = ProjectSettingsResponse(project_id="test_project_id")
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(UpdateProjectSettingsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).project_settings.update(
        contact_settings={"unified_contact_id_enabled": False}
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ProjectSettingsRequest)
    assert request_data.contact_settings.unified_contact_id_enabled is False
    assert isinstance(response, ProjectSettingsResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_project_settings_update_expects_explicit_none_kept(
    mock_sinch_client_conversation, mocker
):
    """Test that an explicit None is kept as a set field on the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = ProjectSettingsResponse()
    spy_endpoint = mocker.spy(UpdateProjectSettingsEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).project_settings.update(
        contact_settings=None
    )

    _, kwargs = spy_endpoint.call_args
    assert "contact_settings" in kwargs["request_data"].model_fields_set
    assert kwargs["request_data"].contact_settings is None


def test_project_settings_update_expects_unset_default():
    """Test that the optional body parameter defaults to the UNSET sentinel."""
    import inspect

    default = (
        inspect.signature(ProjectSettings.update)
        .parameters["contact_settings"]
        .default
    )
    assert default is UNSET


def test_project_settings_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete builds the empty request model and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteProjectSettingsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).project_settings.delete()

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], DeleteProjectSettingsRequest)
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
