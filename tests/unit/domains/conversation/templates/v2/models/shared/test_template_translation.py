import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationCardMessage,
    TemplateTranslationCarouselMessage,
    TemplateTranslationChoiceMessage,
    TemplateTranslationContactInfoMessage,
    TemplateTranslationListMessage,
    TemplateTranslationLocationMessage,
    TemplateTranslationMediaMessage,
    TemplateTranslationTemplateMessage,
    TemplateTranslation,
    TemplateTranslationTextMessage,
)

TEMPLATE_TRANSLATION_ADAPTER = TypeAdapter(TemplateTranslation)


@pytest.mark.parametrize(
    "message_field, message, expected_class",
    [
        ("card_message", {"title": "Card title"}, TemplateTranslationCardMessage),
        (
            "carousel_message",
            {"cards": [{"title": "Card title"}]},
            TemplateTranslationCarouselMessage,
        ),
        (
            "choice_message",
            {
                "choices": [
                    {"text_message": {"text": "Yes"}, "postback_data": "yes"}
                ]
            },
            TemplateTranslationChoiceMessage,
        ),
        (
            "location_message",
            {
                "title": "Phare d'Eckmühl",
                "coordinates": {"latitude": 47.79819, "longitude": -4.3727684},
            },
            TemplateTranslationLocationMessage,
        ),
        (
            "media_message",
            {"url": "https://example.com/image.jpg"},
            TemplateTranslationMediaMessage,
        ),
        (
            "template_message",
            {
                "omni_template": {
                    "template_id": "01HVN010MG3B9N6X323JAFN59P",
                    "version": "1",
                }
            },
            TemplateTranslationTemplateMessage,
        ),
        ("text_message", {"text": "Hello"}, TemplateTranslationTextMessage),
        (
            "list_message",
            {
                "title": "Choose your icecream flavor",
                "sections": [
                    {
                        "items": [
                            {
                                "choice": {
                                    "title": "Strawberry",
                                    "postback_data": "Strawberry postback",
                                }
                            }
                        ]
                    }
                ],
            },
            TemplateTranslationListMessage,
        ),
        (
            "contact_info_message",
            {
                "name": {"full_name": "John Doe"},
                "phone_numbers": [{"phone_number": "+15551231234"}],
            },
            TemplateTranslationContactInfoMessage,
        ),
    ],
)
def test_template_translation_expects_message_type_variant(
    message_field, message, expected_class
):
    """Test that each oneOf message type resolves to its translation variant."""
    model = TEMPLATE_TRANSLATION_ADAPTER.validate_python(
        {"language_code": "en-US", "version": "1", message_field: message}
    )

    assert isinstance(model, expected_class)
    assert model.language_code == "en-US"
    assert model.version == "1"
    assert getattr(model, message_field) is not None

    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert message_field in alias_dump


def test_template_translation_expects_missing_message_rejected():
    """Test that a translation without any message type is rejected."""
    with pytest.raises(ValidationError):
        TEMPLATE_TRANSLATION_ADAPTER.validate_python(
            {"language_code": "en-US", "version": "1"}
        )
