import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    DeleteTemplateEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)


@pytest.fixture
def request_data():
    return TemplateIdRequest(template_id="01HVN010MG3B9N6X323JAFN59P")


@pytest.fixture
def mock_response():
    return HTTPResponse(status_code=204, body=None, headers={})


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "code": 404,
                "message": "Template not found",
                "status": "NOT_FOUND",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return DeleteTemplateEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the template_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.template.api.sinch.com/v2/projects/test_project_id/templates/01HVN010MG3B9N6X323JAFN59P"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that no body is sent."""
    assert endpoint.request_body() is None


def test_handle_response_expects_no_return_model(endpoint, mock_response):
    """Test that a successful delete does not return a response model."""
    assert endpoint.handle_response(mock_response) is None


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Template not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 404
