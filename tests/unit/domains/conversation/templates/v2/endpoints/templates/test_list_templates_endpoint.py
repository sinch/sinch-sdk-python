from datetime import datetime, timezone
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    ListTemplatesEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_request import (
    ListTemplatesRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_response import (
    ListTemplatesResponse,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationTextMessage,
)


@pytest.fixture
def request_data():
    return ListTemplatesRequest()


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={"templates": [{
            "id": "01HVN010MG3B9N6X323JAFN59P",
            "description": "Text template V2",
            "version": 1,
            "default_translation": "en-US",
            "translations": [
                {
                    "language_code": "en-US",
                    "version": "3",
                    "create_time": "2024-06-06T14:42:42Z",
                    "update_time": "2024-06-06T14:42:42Z",
                    "variables": [
                        {"key": "name", "preview_value": "Professor Jones"}
                    ],
                    "text_message": {"text": "Hello ${name}"},
                    "channel_template_overrides": {},
                }
            ],
            "create_time": "2024-06-06T14:42:42Z",
            "update_time": "2024-06-06T14:42:42Z",
            "extra_field": "extra_value",
        }]},
        headers={"Content-Type": "application/json"},
    )


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
    return ListTemplatesEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the templates origin."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.template.api.sinch.com/v2/projects/test_project_id/templates"
    )


def test_build_query_params_expects_empty(endpoint):
    """Test that no query params are sent."""
    assert endpoint.build_query_params() == {}


def test_request_body_expects_no_body(endpoint):
    """Test that no body is sent."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped to ListTemplatesResponse."""
    response = endpoint.handle_response(mock_response)

    assert isinstance(response, ListTemplatesResponse)
    parsed = response.templates[0]
    assert isinstance(parsed, TemplateResponse)
    assert parsed.id == "01HVN010MG3B9N6X323JAFN59P"
    assert parsed.description == "Text template V2"
    assert parsed.version == 1
    assert parsed.default_translation == "en-US"
    assert parsed.create_time == datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc)
    assert parsed.update_time == datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc)
    translation = parsed.translations[0]
    assert isinstance(translation, TemplateTranslationTextMessage)
    assert translation.language_code == "en-US"
    assert translation.version == "3"
    assert translation.text_message.text == "Hello ${name}"
    assert translation.variables[0].key == "name"
    assert translation.variables[0].preview_value == "Professor Jones"
    assert translation.channel_template_overrides == {}


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Template not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 404
