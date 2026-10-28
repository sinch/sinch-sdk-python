import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.templates.api.v2.internal.templates_endpoints import (
    ListTranslationsEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_request import (
    ListTranslationsRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_response import (
    ListTranslationsResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationLocationMessage,
    TemplateTranslationTextMessage,
)


@pytest.fixture
def request_data():
    return ListTranslationsRequest(
        template_id="01W4FFL35P4NC4K35TEMPLATEV2",
        language_code="en-US",
        translation_version="1",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "translations": [
                {
                    "language_code": "en-US",
                    "version": "1",
                    "text_message": {"text": "Message from a template v2."},
                },
                {
                    "language_code": "fr-FR",
                    "version": "1",
                    "location_message": {
                        "title": "Phare d'Eckmühl",
                        "coordinates": {
                            "latitude": 47.79819,
                            "longitude": -4.3727684,
                        },
                        "label": "Pointe de Penmarch",
                    },
                },
            ]
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
    return ListTranslationsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_conversation):
    """Test that the URL is built correctly with the template_id path param."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.template.api.sinch.com/v2/projects/test_project_id/templates/01W4FFL35P4NC4K35TEMPLATEV2/translations"
    )


def test_build_query_params_expects_all_query_fields(endpoint):
    """Test that the query params contain the language code and translation version."""
    assert endpoint.build_query_params() == {
        "language_code": "en-US",
        "translation_version": "1",
    }


def test_build_query_params_expects_none_fields_excluded():
    """Test that a query field passed as None is not sent."""
    endpoint = ListTranslationsEndpoint(
        "test_project_id",
        ListTranslationsRequest(
            template_id="01W4FFL35P4NC4K35TEMPLATEV2",
            language_code=None,
            translation_version="1",
        ),
    )

    assert endpoint.build_query_params() == {"translation_version": "1"}



def test_request_body_expects_no_body(endpoint):
    """Test that query and path params never leak into the body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that each translation resolves to its message type variant."""
    response = endpoint.handle_response(mock_response)

    assert isinstance(response, ListTranslationsResponse)
    text, location = response.translations
    assert isinstance(text, TemplateTranslationTextMessage)
    assert text.language_code == "en-US"
    assert text.version == "1"
    assert text.text_message.text == "Message from a template v2."
    assert isinstance(location, TemplateTranslationLocationMessage)
    assert location.language_code == "fr-FR"
    assert location.location_message.title == "Phare d'Eckmühl"
    assert location.location_message.coordinates.latitude == 47.79819
    assert location.location_message.label == "Pointe de Penmarch"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised when the server returns an error."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Template not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 404
