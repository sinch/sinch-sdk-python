import pytest
from pydantic import ValidationError

from sinch.domains.conversation.templates.models.v2.internal.update_template_request import (
    UpdateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationListMessage,
)


def test_update_template_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UpdateTemplateRequest(
        template_id="01HVN010MG3B9N6X323JAFN59P",
        version=1,
        description="Updated description v2",
        default_translation="en-US",
        translations=[
            {
                "language_code": "en-US",
                "list_message": {
                    "title": "Choose your icecream flavor",
                    "sections": [
                        {
                            "title": "Fruit flavors",
                            "items": [
                                {
                                    "choice": {
                                        "title": "Strawberry",
                                        "postback_data": "Strawberry postback",
                                    }
                                }
                            ],
                        }
                    ],
                },
            }
        ],
    )

    assert model.template_id == "01HVN010MG3B9N6X323JAFN59P"
    assert model.version == 1
    assert model.description == "Updated description v2"
    assert model.default_translation == "en-US"
    assert isinstance(model.translations[0], TemplateTranslationListMessage)
    assert model.translations[0].list_message.title == "Choose your icecream flavor"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["version"] == 1
    assert alias_dump["description"] == "Updated description v2"


def test_update_template_request_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = UpdateTemplateRequest(
        template_id="01HVN010MG3B9N6X323JAFN59P",
        version=1,
    )

    assert model.description is None
    assert model.default_translation is None
    assert model.translations is None


def test_update_template_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        UpdateTemplateRequest(
            template_id="01HVN010MG3B9N6X323JAFN59P",
            )
