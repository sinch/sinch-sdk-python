"""
Unit tests for Conversation Templates API
"""
import pytest
from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.templates.api.v2.templates_apis import (
    Templates,
)
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    CreateTemplateEndpoint,
    DeleteTemplateEndpoint,
    GetTemplateEndpoint,
    ListTemplatesEndpoint,
    ListTranslationsEndpoint,
    UpdateTemplateEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.create_template_request import (
    CreateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_request import (
    ListTemplatesRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_response import (
    ListTemplatesResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_request import (
    ListTranslationsRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_response import (
    ListTranslationsResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.update_template_request import (
    UpdateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationLocationMessage,
    TemplateTranslationTextMessage,
)

TEMPLATE_ID = "01HVN010MG3B9N6X323JAFN59P"


@pytest.fixture
def text_translation():
    return {
        "language_code": "en-US",
        "version": "1",
        "variables": [{"key": "name", "preview_value": "Professor Jones"}],
        "text_message": {"text": "Hello ${name}"},
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


@pytest.fixture
def mock_template_response():
    return TemplateResponse(
        id=TEMPLATE_ID,
        description="Text template V2",
        version=1,
        default_translation="en-US",
    )


def test_conversation_expects_templates_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .templates as a Templates instance."""
    conversation = Conversation(mock_sinch_client_conversation)
    assert isinstance(conversation.templates, Templates)


def test_templates_create_expects_correct_request(
    mock_sinch_client_conversation,
    mock_template_response,
    text_translation,
    mocker,
):
    """Test that create sends the correct request with all parameters and returns TemplateResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_template_response
    spy_endpoint = mocker.spy(CreateTemplateEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).templates.create(
        default_translation="en-US",
        translations=[text_translation],
        id=TEMPLATE_ID,
        description="Text template V2",
        version=1,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, CreateTemplateRequest)
    assert request_data.id == TEMPLATE_ID
    assert request_data.description == "Text template V2"
    assert request_data.version == 1
    assert request_data.default_translation == "en-US"
    translation = request_data.translations[0]
    assert isinstance(translation, TemplateTranslationTextMessage)
    assert translation.language_code == "en-US"
    assert translation.version == "1"
    assert translation.text_message.text == "Hello ${name}"
    assert translation.variables[0].key == "name"
    assert translation.variables[0].preview_value == "Professor Jones"
    override = translation.channel_template_overrides["WHATSAPP"]
    assert override.template_reference.template_id == "whatsapp_template"
    assert override.parameter_mappings == {"body[1]text": "name"}
    assert isinstance(response, TemplateResponse)
    assert response.id == TEMPLATE_ID
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_create_expects_omitted_optionals_unset(
    mock_sinch_client_conversation,
    mock_template_response,
    text_translation,
    mocker,
):
    """Test that omitted optional parameters never reach the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_template_response
    spy_endpoint = mocker.spy(CreateTemplateEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).templates.create(
        default_translation="en-US",
        translations=[text_translation],
    )

    _, kwargs = spy_endpoint.call_args
    assert "id" not in kwargs["request_data"].model_fields_set
    assert "description" not in kwargs["request_data"].model_fields_set
    assert "version" not in kwargs["request_data"].model_fields_set


def test_templates_delete_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that delete sends the correct request and returns None."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = None
    spy_endpoint = mocker.spy(DeleteTemplateEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).templates.delete(
        template_id=TEMPLATE_ID
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], TemplateIdRequest)
    assert kwargs["request_data"].template_id == TEMPLATE_ID
    assert response is None
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_get_expects_correct_request(
    mock_sinch_client_conversation, mock_template_response, mocker
):
    """Test that get sends the correct request and returns TemplateResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_template_response
    spy_endpoint = mocker.spy(GetTemplateEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).templates.get(
        template_id=TEMPLATE_ID
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], TemplateIdRequest)
    assert kwargs["request_data"].template_id == TEMPLATE_ID
    assert isinstance(response, TemplateResponse)
    assert response.id == TEMPLATE_ID
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_list_expects_correct_request(
    mock_sinch_client_conversation, mock_template_response, mocker
):
    """Test that list sends the correct request and returns a single-page TokenBasedPaginator."""
    mock_response = ListTemplatesResponse(templates=[mock_template_response])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListTemplatesEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).templates.list()

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(kwargs["request_data"], ListTemplatesRequest)
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    assert response.has_next_page is False
    templates = response.content()
    assert len(templates) == 1
    assert isinstance(templates[0], TemplateResponse)
    assert templates[0].id == TEMPLATE_ID
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_list_expects_empty_content_when_no_templates(
    mock_sinch_client_conversation,
):
    """Test that the paginator content is empty when the response has no templates."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = ListTemplatesResponse()

    response = Conversation(mock_sinch_client_conversation).templates.list()

    assert response.content() == []


def test_templates_list_translations_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list_translations sends the correct request and returns a single-page TokenBasedPaginator."""
    mock_response = ListTranslationsResponse(
        translations=[
            {
                "language_code": "fr-FR",
                "version": "1",
                "location_message": {
                    "title": "Phare d'Eckmühl",
                    "coordinates": {
                        "latitude": 47.79819,
                        "longitude": -4.3727684,
                    },
                },
            }
        ]
    )
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListTranslationsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).templates.list_translations(
        template_id=TEMPLATE_ID,
        language_code="fr-FR",
        translation_version="1",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ListTranslationsRequest)
    assert request_data.template_id == TEMPLATE_ID
    assert request_data.language_code == "fr-FR"
    assert request_data.translation_version == "1"
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    assert response.has_next_page is False
    translations = response.content()
    assert len(translations) == 1
    assert isinstance(translations[0], TemplateTranslationLocationMessage)
    assert translations[0].location_message.title == "Phare d'Eckmühl"
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_list_translations_expects_empty_content_when_no_translations(
    mock_sinch_client_conversation,
):
    """Test that the paginator content is empty when the response has no translations."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = ListTranslationsResponse()

    response = Conversation(
        mock_sinch_client_conversation
    ).templates.list_translations(template_id=TEMPLATE_ID)

    assert response.content() == []


def test_templates_update_expects_correct_request(
    mock_sinch_client_conversation,
    mock_template_response,
    text_translation,
    mocker,
):
    """Test that update sends the correct request with all parameters and returns TemplateResponse."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_template_response
    spy_endpoint = mocker.spy(UpdateTemplateEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).templates.update(
        template_id=TEMPLATE_ID,
        version=1,
        default_translation="en-US",
        translations=[text_translation],
        description="Updated description v2",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, UpdateTemplateRequest)
    assert request_data.template_id == TEMPLATE_ID
    assert request_data.version == 1
    assert request_data.default_translation == "en-US"
    assert request_data.description == "Updated description v2"
    assert isinstance(request_data.translations[0], TemplateTranslationTextMessage)
    assert request_data.translations[0].text_message.text == "Hello ${name}"
    assert isinstance(response, TemplateResponse)
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_templates_update_expects_omitted_optionals_unset(
    mock_sinch_client_conversation, mock_template_response, mocker
):
    """Test that omitted optional parameters never reach the request model."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_template_response
    spy_endpoint = mocker.spy(UpdateTemplateEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).templates.update(
        template_id=TEMPLATE_ID, version=1
    )

    _, kwargs = spy_endpoint.call_args
    fields_set = kwargs["request_data"].model_fields_set
    assert "default_translation" not in fields_set
    assert "translations" not in fields_set
    assert "description" not in fields_set
