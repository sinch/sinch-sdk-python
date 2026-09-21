import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TemplateAppMessage,
)


@pytest.fixture
def template_app_message_with_omni_override_template_reference_data():
    return {
        "template_message": {
            "channel_template": {
                "KAKAOTALK": {
                    "template_id": "my template ID value",
                    "language_code": "en-US"
                }
            },
            "omni_template": {
                "template_id": "another template ID",
                "version": "another version",
                "language_code": "another language",
                "parameters": {
                    "name": "Value for the name parameter used in the version 1 and language \"en-US\" of the template"
                }
            }
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "template_reference": {
                    "template_id": "another template ID",
                    "version": "another version",
                    "language_code": "another language",
                    "parameters": {
                        "name": "Value for the name parameter used in the version 1 and language \"en-US\" of the template"
                    }
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_template_app_message_with_omni_override_template_reference_expects_correct_fields(
    template_app_message_with_omni_override_template_reference_data,
):
    """Test that TemplateAppMessage with OmniMessageOverrideTemplateReference is parsed correctly."""
    parsed_response = TemplateAppMessage.model_validate(
        template_app_message_with_omni_override_template_reference_data
    )

    assert isinstance(parsed_response, TemplateAppMessage)
    assert parsed_response.template_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.template_reference is not None
    assert omni_override.template_reference.template_id == "another template ID"
    assert omni_override.template_reference.version == "another version"
    assert omni_override.template_reference.language_code == "another language"
    assert omni_override.template_reference.parameters is not None
    assert omni_override.template_reference.parameters["name"] == "Value for the name parameter used in the version 1 and language \"en-US\" of the template"
    assert parsed_response.agent is not None
