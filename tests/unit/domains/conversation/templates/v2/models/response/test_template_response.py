from datetime import datetime, timezone

from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationTextMessage,
)


def test_template_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TemplateResponse(
        id="01HVN010MG3B9N6X323JAFN59P",
        description="Text template V2",
        version=1,
        default_translation="en-US",
        translations=[
            {"language_code": "en-US", "text_message": {"text": "Hi"}}
        ],
        create_time="2024-06-06T14:42:42Z",
        update_time="2024-06-06T15:45:45Z",
    )

    assert model.id == "01HVN010MG3B9N6X323JAFN59P"
    assert model.description == "Text template V2"
    assert model.version == 1
    assert model.default_translation == "en-US"
    assert isinstance(model.translations[0], TemplateTranslationTextMessage)
    assert model.create_time == datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc)
    assert model.update_time == datetime(2024, 6, 6, 15, 45, 45, tzinfo=timezone.utc)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["id"] == "01HVN010MG3B9N6X323JAFN59P"
    assert alias_dump["default_translation"] == "en-US"


def test_template_response_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = TemplateResponse()

    assert model.id is None
    assert model.description is None
    assert model.version is None
    assert model.default_translation is None
    assert model.translations is None
    assert model.create_time is None
    assert model.update_time is None
