import pytest
from pydantic import ValidationError

from sinch.domains.conversation.templates.models.v2.internal.list_translations_request import (
    ListTranslationsRequest,
)


def test_list_translations_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListTranslationsRequest(
        template_id="01HVN010MG3B9N6X323JAFN59P",
        language_code="en-US",
        translation_version="latest",
    )

    assert model.template_id == "01HVN010MG3B9N6X323JAFN59P"
    assert model.language_code == "en-US"
    assert model.translation_version == "latest"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["language_code"] == "en-US"
    assert alias_dump["translation_version"] == "latest"


def test_list_translations_request_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ListTranslationsRequest(template_id="01HVN010MG3B9N6X323JAFN59P")

    assert model.language_code is None
    assert model.translation_version is None


def test_list_translations_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        ListTranslationsRequest(language_code="en-US")
