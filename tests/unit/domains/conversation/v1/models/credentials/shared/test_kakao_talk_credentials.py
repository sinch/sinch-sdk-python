import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.kakao_talk_credentials import (
    KakaoTalkCredentials,
)


def test_kakao_talk_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = KakaoTalkCredentials(
        kakaotalk_plus_friend_id="friend-id",
        kakaotalk_sender_key="sender-key",
    )

    assert model.kakaotalk_plus_friend_id == "friend-id"
    assert model.kakaotalk_sender_key == "sender-key"


@pytest.mark.parametrize(
    "missing", ["kakaotalk_plus_friend_id", "kakaotalk_sender_key"]
)
def test_kakao_talk_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {
        "kakaotalk_plus_friend_id": "friend-id",
        "kakaotalk_sender_key": "sender-key",
    }
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        KakaoTalkCredentials(**data)

    assert missing in str(excinfo.value)
