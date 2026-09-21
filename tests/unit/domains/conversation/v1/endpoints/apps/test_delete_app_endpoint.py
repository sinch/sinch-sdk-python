import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.apps_endpoints import (
    DeleteAppEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)


@pytest.fixture
def request_data():
    return AppIdRequest(app_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={},
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
    return DeleteAppEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the app_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_expects_no_return_model(endpoint, mock_response):
    """Test that a successful delete does not return a response model."""
    assert endpoint.handle_response(mock_response) is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
