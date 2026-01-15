import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.internal import DeleteMessageEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import MessageIdRequest
from sinch.domains.conversation.api.v1.exceptions import ConversationException


@pytest.fixture
def request_data():
    return MessageIdRequest(message_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=204,
        body=None,
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "message": "Message not found",
                "status": "NotFound"
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return DeleteMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """
    Test that the URL is built correctly.
    """
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com//v1/projects/test_project_id/messages/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_messages_source_query_param_expects_parsed_params():
    """
    Test that the messages_source query parameter is parsed correctly.
    """
    request_data = MessageIdRequest(
        message_id="01FC66621XXXXX119Z8PMV1QPQ",
        messages_source="CONVERSATION_SOURCE"
    )
    endpoint = DeleteMessageEndpoint("test_project_id", request_data)
    
    query_params = endpoint.build_query_params()
    assert query_params["messages_source"] == "CONVERSATION_SOURCE"


def test_handle_response_expects_success(endpoint, mock_response):
    """
    Test that a successful delete response (204 No Content) is handled correctly.
    """
    result = endpoint.handle_response(mock_response)
    assert result is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """
    Test that ConversationException is raised when server returns an error.
    """
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
