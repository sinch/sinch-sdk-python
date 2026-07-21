import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    ConversationChannelCredentials,
    StaticBearerChannelCredentials,
    StaticTokenChannelCredentials,
    MMSChannelCredentials,
    KakaoTalkChannelCredentials,
    TelegramChannelCredentials,
    LineChannelCredentials,
    LineEnterpriseChannelCredentials,
    WeChatChannelCredentials,
    InstagramChannelCredentials,
    AppleBusinessChatChannelCredentials,
    KakaoTalkChatChannelCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_thailand import (
    LineEnterpriseCredentialsThailand,
)

adapter = TypeAdapter(ConversationChannelCredentials)


@pytest.mark.parametrize(
    "payload, expected_class",
    [
        (
            {"channel": "SMS", "static_bearer": {"claimed_identity": "ci", "token": "t"}},
            StaticBearerChannelCredentials,
        ),
        (
            {"channel": "MESSENGER", "static_token": {"token": "t"}},
            StaticTokenChannelCredentials,
        ),
        (
            {"channel": "MMS", "mms_credentials": {"account_id": "a", "api_key": "k"}},
            MMSChannelCredentials,
        ),
        (
            {
                "channel": "KAKAOTALK",
                "kakaotalk_credentials": {
                    "kakaotalk_plus_friend_id": "f",
                    "kakaotalk_sender_key": "s",
                },
            },
            KakaoTalkChannelCredentials,
        ),
        (
            {"channel": "TELEGRAM", "telegram_credentials": {"token": "t"}},
            TelegramChannelCredentials,
        ),
        (
            {"channel": "LINE", "line_credentials": {"token": "t", "secret": "s"}},
            LineChannelCredentials,
        ),
        (
            {
                "channel": "WECHAT",
                "wechat_credentials": {
                    "app_id": "a",
                    "app_secret": "s",
                    "token": "t",
                    "aes_key": "k",
                },
            },
            WeChatChannelCredentials,
        ),
        (
            {"channel": "INSTAGRAM", "instagram_credentials": {"token": "t"}},
            InstagramChannelCredentials,
        ),
        (
            {
                "channel": "APPLEBC",
                "applebc_credentials": {"business_chat_account_id": "b"},
            },
            AppleBusinessChatChannelCredentials,
        ),
        (
            {
                "channel": "KAKAOTALKCHAT",
                "kakaotalkchat_credentials": {"kakaotalk_plus_friend_id": "f"},
            },
            KakaoTalkChatChannelCredentials,
        ),
    ],
)
def test_conversation_channel_credentials_expects_union_resolves_to_wrapper(payload, expected_class):
    """Test that each channel-specific payload resolves to its matching wrapper class."""
    result = adapter.validate_python(payload)

    assert isinstance(result, expected_class)


def test_conversation_channel_credentials_expects_line_enterprise_japan_resolution():
    """Test that a line_enterprise payload with line_japan resolves the nested Japan union."""
    result = adapter.validate_python(
        {
            "channel": "LINE",
            "line_enterprise_credentials": {"line_japan": {"token": "t", "secret": "s"}},
        }
    )

    assert isinstance(result, LineEnterpriseChannelCredentials)
    assert isinstance(
        result.line_enterprise_credentials, LineEnterpriseCredentialsJapan
    )
    assert result.line_enterprise_credentials.line_japan.token == "t"


def test_conversation_channel_credentials_expects_line_enterprise_thailand_resolution():
    """Test that a line_enterprise payload with line_thailand resolves the nested Thailand union."""
    result = adapter.validate_python(
        {
            "channel": "LINE",
            "line_enterprise_credentials": {"line_thailand": {"token": "t", "secret": "s"}},
        }
    )

    assert isinstance(result, LineEnterpriseChannelCredentials)
    assert isinstance(
        result.line_enterprise_credentials, LineEnterpriseCredentialsThailand
    )
    assert result.line_enterprise_credentials.line_thailand.token == "t"


def test_conversation_channel_credentials_expects_common_fields_parsed():
    """Test that the shared common fields are parsed alongside the channel-specific field."""
    result = adapter.validate_python(
        {
            "channel": "SMS",
            "static_bearer": {"claimed_identity": "ci", "token": "t"},
            "callback_secret": "secret",
            "credential_ordinal_number": 0,
        }
    )

    assert isinstance(result, StaticBearerChannelCredentials)
    assert result.static_bearer.token == "t"
    assert result.channel == "SMS"
    assert result.callback_secret == "secret"
    assert result.credential_ordinal_number == 0


def test_conversation_channel_credentials_expects_validation_error_without_channel():
    """Test that a payload missing the discriminator 'channel' key fails to resolve."""
    with pytest.raises(ValidationError):
        adapter.validate_python({"static_bearer": {"claimed_identity": "ci", "token": "t"}})


def test_conversation_channel_credentials_expects_validation_error_when_sms_uses_static_token():
    """Test that SMS (a static_bearer channel) rejects a static_token payload instead of
    silently falling into StaticTokenChannelCredentials.
    """
    with pytest.raises(ValidationError) as excinfo:
        adapter.validate_python({"channel": "SMS", "static_token": {"token": "t"}})

    assert "static_bearer" in str(excinfo.value)
