from sinch.domains.conversation.models.v1.messages.categories.template.template_reference_channel_specific import (
    TemplateReferenceChannelSpecific,
)
from sinch.domains.conversation.templates.models.v2.shared.channel_template_override import (
    ChannelTemplateOverride,
)


def test_channel_template_override_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ChannelTemplateOverride(
        template_reference={
            "template_id": "whatsapp_template",
            "version": "1",
            "language_code": "en_US",
            "parameters": {"body[1]text": "defaultValue"},
        },
        parameter_mappings={"body[1]text": "name"},
    )

    assert isinstance(model.template_reference, TemplateReferenceChannelSpecific)
    assert model.template_reference.template_id == "whatsapp_template"
    assert model.template_reference.parameters == {"body[1]text": "defaultValue"}
    assert model.parameter_mappings == {"body[1]text": "name"}

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["template_reference"]["template_id"] == "whatsapp_template"
    assert alias_dump["parameter_mappings"] == {"body[1]text": "name"}


def test_channel_template_override_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ChannelTemplateOverride()

    assert model.template_reference is None
    assert model.parameter_mappings is None
