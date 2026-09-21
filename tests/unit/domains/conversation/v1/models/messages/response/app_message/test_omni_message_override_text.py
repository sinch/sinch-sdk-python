import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    TextAppMessage,
)


@pytest.fixture
def text_app_message_with_omni_override_text_data():
    return {
        "text_message": {
            "text": "This is a text message."
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "text_message": {
                    "text": "This is a text message."
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_text_app_message_with_omni_override_text_expects_correct_fields(
    text_app_message_with_omni_override_text_data,
):
    """Test that TextAppMessage with OmniMessageOverrideText is parsed correctly."""
    parsed_response = TextAppMessage.model_validate(
        text_app_message_with_omni_override_text_data
    )

    assert isinstance(parsed_response, TextAppMessage)
    assert parsed_response.text_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.text_message is not None
    assert omni_override.text_message.text == "This is a text message."
    assert parsed_response.agent is not None
