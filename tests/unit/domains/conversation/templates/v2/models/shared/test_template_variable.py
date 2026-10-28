from sinch.domains.conversation.templates.models.v2.shared.template_variable import (
    TemplateVariable,
)


def test_template_variable_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TemplateVariable(key="name", preview_value="Professor Jones")

    assert model.key == "name"
    assert model.preview_value == "Professor Jones"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["preview_value"] == "Professor Jones"


def test_template_variable_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = TemplateVariable()

    assert model.key is None
    assert model.preview_value is None
