from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.templates.models.v2.shared.channel_template_override import (
    ChannelTemplateOverride,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation_base import (
    TemplateTranslationBase,
)
from sinch.domains.conversation.templates.models.v2.shared.template_variable import (
    TemplateVariable,
)


def test_template_translation_base_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TemplateTranslationBase(
        language_code="en-US",
        version="1",
        channel_template_overrides={
            "WHATSAPP": {
                "template_reference": {"template_id": "whatsapp_template"},
                "parameter_mappings": {"body[1]text": "name"},
            }
        },
        variables=[{"key": "name", "preview_value": "Mr Jones"}],
        create_time="2024-02-08T13:53:48Z",
        update_time="2024-02-08T13:53:48Z",
    )

    assert model.language_code == "en-US"
    assert model.version == "1"
    assert isinstance(
        model.channel_template_overrides["WHATSAPP"], ChannelTemplateOverride
    )
    assert isinstance(model.variables[0], TemplateVariable)
    assert model.variables[0].key == "name"
    assert model.create_time == datetime(2024, 2, 8, 13, 53, 48, tzinfo=timezone.utc)
    assert model.update_time == datetime(2024, 2, 8, 13, 53, 48, tzinfo=timezone.utc)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["language_code"] == "en-US"
    assert alias_dump["channel_template_overrides"]["WHATSAPP"]["parameter_mappings"] == {
        "body[1]text": "name"
    }


def test_template_translation_base_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = TemplateTranslationBase(language_code="en-US")

    assert model.version is None
    assert model.channel_template_overrides is None
    assert model.variables is None
    assert model.create_time is None
    assert model.update_time is None


def test_template_translation_base_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        TemplateTranslationBase(version="1")
