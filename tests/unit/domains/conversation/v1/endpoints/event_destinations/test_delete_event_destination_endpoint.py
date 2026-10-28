import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.event_destinations_endpoints import (
    DeleteEventDestinationEndpoint,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.event_destination_id_request import (
    EventDestinationIdRequest,
)


@pytest.fixture
def request_data():
    return EventDestinationIdRequest(
        event_destination_id="01W4FFL35P4NC4K35WEBHOOK001"
    )


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
    return DeleteEventDestinationEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly with the event destination ID path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/webhooks/01W4FFL35P4NC4K35WEBHOOK001"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a DELETE request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_no_return_model(endpoint, mock_response):
    """Test that a successful delete does not return a response model."""
    assert endpoint.handle_response(mock_response) is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
