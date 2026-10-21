from datetime import datetime, timezone
import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    UpdateTemplateEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.update_template_request import (
    UpdateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationTextMessage,
)


@pytest.fixture
def request_data():
    return UpdateTemplateRequest(
        template_id="01HVN010MG3B9N6X323JAFN59P",
        version=1,
        description="Updated description v2",
        default_translation="en-US",
        translations=[
            {
                "language_code": "en-US",
                "version": "1",
                "variables": [{"key": "name", "preview_value": "Mr Jones"}],
                "text_message": {"text": "Hi ${name}"},
                "channel_template_overrides": {
                    "WHATSAPP": {
                        "template_reference": {
                            "template_id": "whatsapp_template",
                            "version": "1",
                            "language_code": "en_US",
                            "parameters": {"body[1]text": "defaultValue"},
                        },
                        "parameter_mappings": {"body[1]text": "name"},
                    }
                },
            }
        ],
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
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
        },
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
    return UpdateTemplateEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the template_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.template.api.sinch.com/v2/projects/test_project_id/templates/01HVN010MG3B9N6X323JAFN59P"
    )


def test_build_query_params_expects_empty(endpoint):
    """Test that no query params are sent."""
    assert endpoint.build_query_params() == {}


def test_request_body_expects_correct_serialization(endpoint):
    """Test that template_id is excluded from the body."""
    body = json.loads(endpoint.request_body())

    assert "project_id" not in body
    assert "template_id" not in body
    assert "id" not in body
    assert body["version"] == 1
    assert body["description"] == "Updated description v2"
    assert body["default_translation"] == "en-US"
    translation = body["translations"][0]
    assert translation["language_code"] == "en-US"
    assert translation["version"] == "1"
    assert translation["variables"] == [
        {"key": "name", "preview_value": "Mr Jones"}
    ]
    assert translation["text_message"] == {"text": "Hi ${name}"}
    assert translation["channel_template_overrides"] == {
        "WHATSAPP": {
            "template_reference": {
                "template_id": "whatsapp_template",
                "version": "1",
                "language_code": "en_US",
                "parameters": {"body[1]text": "defaultValue"},
            },
            "parameter_mappings": {"body[1]text": "name"},
        }
    }


def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = UpdateTemplateEndpoint(
        "test_project_id",
        UpdateTemplateRequest(
            template_id="01HVN010MG3B9N6X323JAFN59P",
                version=2,
            description=None,
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["version"] == 2
    assert body["description"] is None
    assert "default_translation" not in body
    assert "translations" not in body


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped to TemplateResponse."""
    parsed = endpoint.handle_response(mock_response)

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
