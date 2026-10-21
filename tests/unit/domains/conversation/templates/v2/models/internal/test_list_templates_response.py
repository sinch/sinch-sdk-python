from sinch.domains.conversation.templates.models.v2.internal.list_templates_response import (
    ListTemplatesResponse,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)


def test_list_templates_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListTemplatesResponse(
        templates=[
            {"id": "01HVN010MG3B9N6X323JAFN59P", "version": 1},
            {"id": "01W4FFL35P4NC4K35TEMPLATEV2", "version": 2},
        ]
    )

    assert len(model.templates) == 2
    assert isinstance(model.templates[0], TemplateResponse)
    assert model.templates[0].id == "01HVN010MG3B9N6X323JAFN59P"
    assert model.templates[1].version == 2
    assert model.content == model.templates

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["templates"][1]["id"] == "01W4FFL35P4NC4K35TEMPLATEV2"


def test_list_templates_response_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ListTemplatesResponse()

    assert model.templates is None


def test_list_templates_response_expects_content_empty_when_list_is_none():
    """Test that content returns an empty list when the list field is None."""
    assert ListTemplatesResponse().content == []
