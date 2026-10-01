from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
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
    WeChatChannelCredentials,
    InstagramChannelCredentials,
    AppleBusinessChatChannelCredentials,
    KakaoTalkChatChannelCredentials,
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


def test_conversation_channel_credentials_expects_unknown_channel_parsed_in_a_response():
    """Test that a channel added to the API later is parsed as SinchRawResponse
    instead of failing the whole app response."""
    payload = {"channel": "SOME_NEW_CHANNEL", "new_credentials": {"token": "t"}}

    with response_parsing_scope():
        credentials = adapter.validate_python(payload)

    assert isinstance(credentials, SinchRawResponse)
    assert credentials.model_dump() == payload
