import pytest
from pydantic import ValidationError

from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)


def test_template_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TemplateIdRequest(template_id="01HVN010MG3B9N6X323JAFN59P")

    assert model.template_id == "01HVN010MG3B9N6X323JAFN59P"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["template_id"] == "01HVN010MG3B9N6X323JAFN59P"


def test_template_id_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        TemplateIdRequest()
