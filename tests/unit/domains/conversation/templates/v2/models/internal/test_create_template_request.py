import pytest
from pydantic import ValidationError

from sinch.domains.conversation.templates.models.v2.internal.create_template_request import (
    CreateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationTextMessage,
)


def test_create_template_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CreateTemplateRequest(
        id="01HVN010MG3B9N6X323JAFN59P",
        description="Text template V2",
        version=1,
        default_translation="en-US",
        translations=[
            {"language_code": "en-US", "text_message": {"text": "Hi"}}
        ],
    )

    assert model.id == "01HVN010MG3B9N6X323JAFN59P"
    assert model.description == "Text template V2"
    assert model.version == 1
    assert model.default_translation == "en-US"
    assert isinstance(model.translations[0], TemplateTranslationTextMessage)
    assert model.translations[0].text_message.text == "Hi"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["id"] == "01HVN010MG3B9N6X323JAFN59P"
    assert alias_dump["version"] == 1
    assert alias_dump["default_translation"] == "en-US"
    assert alias_dump["translations"][0]["text_message"] == {"text": "Hi"}


def test_create_template_request_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = CreateTemplateRequest(
        default_translation="en-US",
        translations=[
            {"language_code": "en-US", "text_message": {"text": "Hi"}}
        ],
    )

    assert model.id is None
    assert model.description is None
    assert model.version is None


def test_create_template_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        CreateTemplateRequest(default_translation="en-US")
