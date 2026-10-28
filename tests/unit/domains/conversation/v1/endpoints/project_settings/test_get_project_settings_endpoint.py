import json

import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException

from sinch.domains.conversation.api.v1.internal.project_settings_endpoints import (
    GetProjectSettingsEndpoint,
)
from sinch.domains.conversation.models.v1.project_settings.internal.get_project_settings_request import (
    GetProjectSettingsRequest,
)
from sinch.domains.conversation.models.v1.project_settings.response.project_settings_response import (
    ProjectSettingsResponse,
)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "project_id": "123coffee-dada-beef-cafe-baadc0de5678",
            "settings": {
                "contact_settings": {"unified_contact_id_enabled": True}
            },
            "extra_field": "extra",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=403,
        body={
            "error": {
                "code": 403,
                "message": "You do not have access to the requested resource.",
                "status": "UNAUTHORIZED",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint():
    return GetProjectSettingsEndpoint(
        "test_project_id", GetProjectSettingsRequest()
    )


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/settings"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that nothing leaks into the body."""
    assert not json.loads(endpoint.request_body() or "{}")


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped onto ProjectSettingsResponse."""
    parsed = endpoint.handle_response(mock_response)

    assert isinstance(parsed, ProjectSettingsResponse)
    assert parsed.project_id == "123coffee-dada-beef-cafe-baadc0de5678"
    assert parsed.settings.contact_settings.unified_contact_id_enabled is True
    assert parsed.extra_field == "extra"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert (
        str(exc_info.value)
        == "You do not have access to the requested resource.  UNAUTHORIZED"
    )
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 403
