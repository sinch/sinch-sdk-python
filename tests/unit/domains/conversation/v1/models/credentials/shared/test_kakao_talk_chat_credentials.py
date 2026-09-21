import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.kakao_talk_chat_credentials import (
    KakaoTalkChatCredentials,
)


def test_kakao_talk_chat_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = KakaoTalkChatCredentials(
        kakaotalk_plus_friend_id="friend-id",
        api_key="api-key",
    )

    assert model.kakaotalk_plus_friend_id == "friend-id"
    assert model.api_key == "api-key"


def test_kakao_talk_chat_credentials_expects_api_key_defaults_to_none():
    """Test that the optional api_key defaults to None."""
    model = KakaoTalkChatCredentials(kakaotalk_plus_friend_id="friend-id")

    assert model.api_key is None


def test_kakao_talk_chat_credentials_expects_validation_error_for_missing_field():
    """Test that a ValidationError is raised when the required field is missing."""
    with pytest.raises(ValidationError) as excinfo:
        KakaoTalkChatCredentials(api_key="api-key")

    assert "kakaotalk_plus_friend_id" in str(excinfo.value)
