from sinch.domains.conversation.templates.models.v2.internal.list_translations_response import (
    ListTranslationsResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationMediaMessage,
    TemplateTranslationTextMessage,
)


def test_list_translations_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListTranslationsResponse(
        translations=[
            {"language_code": "en-US", "text_message": {"text": "Hi"}},
            {
                "language_code": "es-ES",
                "media_message": {"url": "https://example.com/image.jpg"},
            },
        ]
    )

    assert isinstance(model.translations[0], TemplateTranslationTextMessage)
    assert isinstance(model.translations[1], TemplateTranslationMediaMessage)
    assert model.translations[1].media_message.url == "https://example.com/image.jpg"
    assert model.content == model.translations

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["translations"][0]["text_message"] == {"text": "Hi"}


def test_list_translations_response_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ListTranslationsResponse()

    assert model.translations is None


def test_list_translations_response_expects_content_empty_when_list_is_none():
    """Test that content returns an empty list when the list field is None."""
    assert ListTranslationsResponse().content == []
