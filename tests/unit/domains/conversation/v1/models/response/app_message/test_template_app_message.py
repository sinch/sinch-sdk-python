import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TemplateAppMessage,
)


@pytest.fixture
def template_app_message_data():
    """Test data for TemplateAppMessage from Java SDK."""
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
        "explicit_channel_message": {
            "KAKAOTALK": "foo value"
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "choice_message": {
                    "text_message": {
                        "text": "This is a text message."
                    },
                    "choices": [
                        {
                            "call_message": {
                                "title": "title value",
                                "phone_number": "phone number value"
                            },
                            "postback_data": "postback call_message data value"
                        }
                    ]
                }
            }
        },
        "channel_specific_message": {
            "MESSENGER": {
                "message_type": "FLOWS",
                "message": {
                    "flow_id": "1",
                    "flow_cta": "Book!",
                    "header": {
                        "type": "text",
                        "text": "text header value"
                    },
                    "body": {
                        "text": "Flow message body"
                    },
                    "footer": {
                        "text": "Flow message footer"
                    },
                    "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s.",
                    "flow_mode": "draft",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "<SCREEN_NAME>",
                        "data": {
                            "product_name": "name",
                            "product_description": "description",
                            "product_price": 100
                        }
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


def test_parsing_template_app_message_expects_correct_fields(template_app_message_data):
    """Test that TemplateAppMessage is parsed correctly with all fields."""
    parsed_response = TemplateAppMessage.model_validate(template_app_message_data)

    assert isinstance(parsed_response, TemplateAppMessage)
    assert parsed_response.template_message is not None
    assert parsed_response.template_message.channel_template is not None
    assert "KAKAOTALK" in parsed_response.template_message.channel_template
    assert parsed_response.template_message.channel_template["KAKAOTALK"].template_id == "my template ID value"
    assert parsed_response.template_message.channel_template["KAKAOTALK"].language_code == "en-US"
    assert parsed_response.template_message.omni_template is not None
    assert parsed_response.template_message.omni_template.template_id == "another template ID"
    assert parsed_response.template_message.omni_template.version == "another version"
    assert parsed_response.template_message.omni_template.language_code == "another language"
    assert parsed_response.template_message.omni_template.parameters is not None
    assert parsed_response.explicit_channel_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert parsed_response.channel_specific_message is not None
    assert parsed_response.agent is not None
