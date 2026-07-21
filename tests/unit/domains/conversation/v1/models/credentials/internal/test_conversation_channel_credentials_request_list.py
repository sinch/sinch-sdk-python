import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.conversation.models.v1.credentials.internal.conversation_channel_credentials_request_list import (
    ConversationChannelCredentialsRequestList,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
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

adapter = TypeAdapter(ConversationChannelCredentialsRequestList)


@pytest.mark.parametrize(
    "payload, expected_class",
    [
        (
            {"SMS": {"claimed_identity": "ci", "token": "t"}},
            StaticBearerChannelCredentials,
        ),
        (
            {"MESSENGER": {"token": "t"}},
            StaticTokenChannelCredentials,
        ),
        (
            {"MMS": {"account_id": "a", "api_key": "k"}},
            MMSChannelCredentials,
        ),
        (
            {
                "KAKAOTALK": {
                    "kakaotalk_plus_friend_id": "f",
                    "kakaotalk_sender_key": "s",
                },
            },
            KakaoTalkChannelCredentials,
        ),
        (
            {"TELEGRAM": {"token": "t"}},
            TelegramChannelCredentials,
        ),
        (
            {"LINE": {"token": "t", "secret": "s"}},
            LineChannelCredentials,
        ),
        (
            {
                "WECHAT": {
                    "app_id": "a",
                    "app_secret": "s",
                    "token": "t",
                    "aes_key": "k",
                },
            },
            WeChatChannelCredentials,
        ),
        (
            {"INSTAGRAM": {"token": "t"}},
            InstagramChannelCredentials,
        ),
        (
            {"APPLEBC": {"business_chat_account_id": "b"}},
            AppleBusinessChatChannelCredentials,
        ),
        (
            {"KAKAOTALKCHAT": {"kakaotalk_plus_friend_id": "f"}},
            KakaoTalkChatChannelCredentials,
        ),
    ],
)
def test_request_list_expects_union_resolves_to_wrapper(payload, expected_class):
    """Test that each channel-keyed payload resolves to its matching wrapper class."""
    result = adapter.validate_python(payload)

    assert len(result) == 1
    assert isinstance(result[0], expected_class)


def test_request_list_expects_line_enterprise_japan_resolution():
    """Test that a LINE_JAPAN payload resolves the nested Japan union."""
    result = adapter.validate_python(
        {"LINE_JAPAN": {"token": "t", "secret": "s", "is_default": True}}
    )

    assert isinstance(result[0], LineEnterpriseChannelCredentials)
    assert isinstance(
        result[0].line_enterprise_credentials, LineEnterpriseCredentialsJapan
    )
    assert result[0].line_enterprise_credentials.line_japan.token == "t"
    assert result[0].line_enterprise_credentials.line_japan.secret == "s"
    assert result[0].line_enterprise_credentials.is_default == True


def test_request_list_expects_line_enterprise_thailand_resolution():
    """Test that a LINE_THAILAND payload resolves the nested Thailand union."""
    result = adapter.validate_python(
        {"LINE_THAILAND": {"token": "t", "secret": "s", "is_default": True}}
    )

    assert isinstance(result[0], LineEnterpriseChannelCredentials)
    assert isinstance(
        result[0].line_enterprise_credentials, LineEnterpriseCredentialsThailand
    )
    assert result[0].line_enterprise_credentials.line_thailand.token == "t"
    assert result[0].line_enterprise_credentials.line_thailand.secret == "s"
    assert result[0].line_enterprise_credentials.is_default == True

def test_request_list_expects_common_fields_parsed():
    """Test that the shared common fields are lifted to the entry level."""
    result = adapter.validate_python(
        {
            "SMS": {
                "claimed_identity": "ci",
                "token": "t",
                "callback_secret": "secret",
                "credential_ordinal_number": 0,
            }
        }
    )

    assert isinstance(result[0], StaticBearerChannelCredentials)
    assert result[0].static_bearer.token == "t"
    assert result[0].channel == "SMS"
    assert result[0].callback_secret == "secret"
    assert result[0].credential_ordinal_number == 0


def test_request_list_expects_multiple_channels_preserving_order():
    """Test that multiple channel entries all resolve, in insertion order."""
    result = adapter.validate_python(
        {
            "SMS": {"claimed_identity": "ci", "token": "t"},
            "MESSENGER": {"token": "fb"},
        }
    )

    assert [type(item).__name__ for item in result] == [
        "StaticBearerChannelCredentials",
        "StaticTokenChannelCredentials",
    ]


def test_request_list_expects_empty_dict_returns_empty_list():
    """Test that an empty channel-keyed dict is valid and yields an empty list."""
    result = adapter.validate_python({})

    assert result == []


def test_request_list_expects_validation_error_for_missing_required_field():
    """Test that a channel missing its required credential field fails validation.

    SMS always maps to static_bearer, so it cannot be routed to the wrong
    wrapper class the way a raw list entry could, but claimed_identity is
    still required and its absence must fail.
    """
    with pytest.raises(ValidationError) as excinfo:
        adapter.validate_python({"SMS": {"token": "t"}})

    assert "claimed_identity" in str(excinfo.value)


def test_request_list_expects_validation_error_for_unsupported_channel():
    """Test that an unrecognized channel key fails validation."""
    with pytest.raises(ValidationError) as excinfo:
        adapter.validate_python({"UNKNOWN": {"token": "x"}})

    assert "Unsupported channel" in str(excinfo.value)


def test_request_list_expects_duplicate_dict_key_keeps_last_value():
    """Test what happens with two 'SMS' keys in the same dict literal.

    A Python dict cannot actually hold two entries with the same key --
    the second one silently overwrites the first before our code ever
    sees the payload. This documents that behavior explicitly: only the
    last SMS value survives, there is no error and no merging.
    """
    payload = {
        "SMS": {"claimed_identity": "first", "token": "a"},
        "SMS": {"claimed_identity": "second", "token": "b"},
    }

    assert payload == {"SMS": {"claimed_identity": "second", "token": "b"}}

    result = adapter.validate_python(payload)

    assert len(result) == 1
    assert result[0].static_bearer.claimed_identity == "second"
    assert result[0].static_bearer.token == "b"
