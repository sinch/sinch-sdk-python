import pytest
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    MediaAppMessage,
)


@pytest.fixture
def media_app_message_with_omni_override_media_data():
    return {
        "media_message": {
            "url": "an url value",
            "thumbnail_url": "another url",
            "filename_override": "filename override value"
        },
        "explicit_channel_omni_message": {
            "KAKAOTALK": {
                "media_message": {
                    "url": "an url value",
                    "thumbnail_url": "another url",
                    "filename_override": "filename override value"
                }
            }
        },
        "agent": {
            "display_name": "display_name value",
            "type": "BOT",
            "picture_url": "picture_url value"
        }
    }


def test_parsing_media_app_message_with_omni_override_media_expects_correct_fields(
    media_app_message_with_omni_override_media_data,
):
    """Test that MediaAppMessage with OmniMessageOverrideMedia is parsed correctly."""
    parsed_response = MediaAppMessage.model_validate(
        media_app_message_with_omni_override_media_data
    )

    assert isinstance(parsed_response, MediaAppMessage)
    assert parsed_response.media_message is not None
    assert parsed_response.explicit_channel_omni_message is not None
    assert "KAKAOTALK" in parsed_response.explicit_channel_omni_message
    omni_override = parsed_response.explicit_channel_omni_message["KAKAOTALK"]
    assert omni_override.media_message is not None
    assert omni_override.media_message.url == "an url value"
    assert omni_override.media_message.thumbnail_url == "another url"
    assert omni_override.media_message.filename_override == "filename override value"
    assert parsed_response.agent is not None
