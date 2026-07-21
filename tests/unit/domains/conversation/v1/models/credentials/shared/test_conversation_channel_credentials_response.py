"""Unit tests for ConversationChannelCredentialsResponse."""
import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials_response import (
    ConversationChannelCredentialsResponse,
    StaticBearerChannelCredentialsResponse,
    StaticTokenChannelCredentialsResponse,
    MMSChannelCredentialsResponse,
    InstagramChannelCredentialsResponse,
    TelegramChannelCredentialsResponse,
    KakaoTalkChannelCredentialsResponse,
    KakaoTalkChatChannelCredentialsResponse,
    LineChannelCredentialsResponse,
    LineEnterpriseJapanChannelCredentialsResponse,
    LineEnterpriseThailandChannelCredentialsResponse,
    WeChatChannelCredentialsResponse,
    AppleBusinessChatChannelCredentialsResponse,
)


def _get_nested(obj, dotted_attr):
    for part in dotted_attr.split("."):
        obj = getattr(obj, part)
    return obj


# (server entry, model field name, expected type, {dotted attr: expected value})
CHANNEL_CASES = [
    (
        {
            "channel": "WHATSAPP",
            "static_bearer": {"claimed_identity": "sp-id", "token": "wa-token"},
        },
        "whatsapp",
        StaticBearerChannelCredentialsResponse,
        {"token": "wa-token"},
    ),
    (
        {
            "channel": "RCS",
            "static_bearer": {"claimed_identity": "sp-id", "token": "rcs-token"},
        },
        "rcs",
        StaticBearerChannelCredentialsResponse,
        {"token": "rcs-token"},
    ),
    (
        {
            "channel": "SMS",
            "static_bearer": {"claimed_identity": "sp-id", "token": "sms-token"},
        },
        "sms",
        StaticBearerChannelCredentialsResponse,
        {"token": "sms-token"},
    ),
    (
        {
            "channel": "VIBERBM",
            "static_bearer": {"claimed_identity": "sp-id", "token": "viber-token"},
        },
        "viberbm",
        StaticBearerChannelCredentialsResponse,
        {"token": "viber-token"},
    ),
    (
        {"channel": "MESSENGER", "static_token": {"token": "fb-token"}},
        "messenger",
        StaticTokenChannelCredentialsResponse,
        {"token": "fb-token"},
    ),
    (
        {
            "channel": "MMS",
            "mms_credentials": {"account_id": "acc", "api_key": "key"},
        },
        "mms",
        MMSChannelCredentialsResponse,
        {"account_id": "acc"},
    ),
    (
        {"channel": "INSTAGRAM", "instagram_credentials": {"token": "ig-token"}},
        "instagram",
        InstagramChannelCredentialsResponse,
        {"token": "ig-token"},
    ),
    (
        {
            "channel": "TELEGRAM",
            "telegram_credentials": {"token": "telegram-token"},
        },
        "telegram",
        TelegramChannelCredentialsResponse,
        {"token": "telegram-token"},
    ),
    (
        {
            "channel": "KAKAOTALK",
            "kakaotalk_credentials": {
                "kakaotalk_plus_friend_id": "friend-id",
                "kakaotalk_sender_key": "sender-key",
            },
        },
        "kakaotalk",
        KakaoTalkChannelCredentialsResponse,
        {"kakaotalk_plus_friend_id": "friend-id"},
    ),
    (
        {
            "channel": "KAKAOTALKCHAT",
            "kakaotalkchat_credentials": {
                "kakaotalk_plus_friend_id": "chat-friend-id"
            },
        },
        "kakaotalkchat",
        KakaoTalkChatChannelCredentialsResponse,
        {"kakaotalk_plus_friend_id": "chat-friend-id"},
    ),
    (
        {
            "channel": "LINE",
            "line_credentials": {"token": "line-token", "secret": "line-secret"},
        },
        "line",
        LineChannelCredentialsResponse,
        {"token": "line-token", "secret": "line-secret"},
    ),
    (
        {
            "channel": "WECHAT",
            "wechat_credentials": {
                "app_id": "wechat-app-id",
                "app_secret": "wechat-app-secret",
                "token": "wechat-token",
                "aes_key": "wechat-aes-key",
            },
        },
        "wechat",
        WeChatChannelCredentialsResponse,
        {"app_id": "wechat-app-id"},
    ),
    (
        {
            "channel": "APPLEBC",
            "applebc_credentials": {"business_chat_account_id": "bca-id"},
        },
        "applebc",
        AppleBusinessChatChannelCredentialsResponse,
        {"business_chat_account_id": "bca-id"},
    ),
]

CHANNEL_CASE_IDS = [
    "WHATSAPP",
    "RCS",
    "SMS",
    "VIBERBM",
    "MESSENGER",
    "MMS",
    "INSTAGRAM",
    "TELEGRAM",
    "KAKAOTALK",
    "KAKAOTALKCHAT",
    "LINE",
    "WECHAT",
    "APPLEBC",
]

CHANNEL_CASE_FIELD_NAMES = {case[1] for case in CHANNEL_CASES}


@pytest.mark.parametrize(
    "entry, field_name, expected_type, checks",
    CHANNEL_CASES,
    ids=CHANNEL_CASE_IDS,
)
def test_response_maps_each_channel_from_server_array(
    entry, field_name, expected_type, checks
):
    """Every branch of the Union is reachable from the server's array format."""
    model = ConversationChannelCredentialsResponse.model_validate([entry])

    value = getattr(model, field_name)
    assert isinstance(value, expected_type)
    for dotted_attr, expected_value in checks.items():
        assert _get_nested(value, dotted_attr) == expected_value

    for other_field_name in CHANNEL_CASE_FIELD_NAMES - {field_name}:
        assert getattr(model, other_field_name) is None


def test_response_line_union_discriminates_japan_variant():
    """A LINE payload carrying line_japan resolves to the Japan variant."""
    model = ConversationChannelCredentialsResponse.model_validate(
        [
            {
                "channel": "LINE",
                "line_enterprise_credentials": {
                    "line_japan": {"token": "tok", "secret": "sec"},
                    "is_default": True,
                },
            }
        ]
    )

    assert isinstance(
        model.line_japan, LineEnterpriseJapanChannelCredentialsResponse
    )
    assert model.line_japan.token == "tok"
    assert model.line_japan.secret == "sec"
    assert model.line_japan.is_default == True



def test_response_line_union_discriminates_thailand_variant():
    """A LINE payload carrying line_thailand resolves to the Thailand variant."""
    model = ConversationChannelCredentialsResponse.model_validate(
        [
            {
                "channel": "LINE",
                "line_enterprise_credentials": {
                    "line_thailand": {"token": "tok", "secret": "sec"}
                },
            }
        ]
    )

    assert isinstance(
        model.line_thailand, LineEnterpriseThailandChannelCredentialsResponse
    )
    assert model.line_thailand.token == "tok"
    assert model.line_thailand.secret == "sec"


def test_response_maps_common_fields_from_server_array():
    """Common fields (callback_secret alias, ordinal, state, known id) are mapped."""
    model = ConversationChannelCredentialsResponse.model_validate(
        [
            {
                "channel": "SMS",
                "static_bearer": {"claimed_identity": "sp-id", "token": "tok"},
                "callback_secret": "secret",
                "credential_ordinal_number": 2,
                "state": {"status": "ACTIVE"},
                "channel_known_id": "known-id",
            }
        ]
    )

    assert model.sms.callback_secret == "secret"
    assert model.sms.credential_ordinal_number == 2
    assert model.sms.state.status == "ACTIVE"
    assert model.sms.channel_known_id == "known-id"



def test_response_expects_empty_list_leaves_all_channels_none():
    """An empty server array is valid and leaves every channel unset."""
    model = ConversationChannelCredentialsResponse.model_validate([])

    assert model.model_dump(exclude_none=True) == {}


def test_response_raises_validation_error_when_sms_uses_static_token():
    """SMS requires static_bearer; static_token is missing claimed_identity."""
    with pytest.raises(ValidationError) as excinfo:
        ConversationChannelCredentialsResponse.model_validate(
            [{"channel": "SMS", "static_token": {"token": "my-token"}}]
        )

    assert "claimed_identity" in str(excinfo.value)


def test_response_raises_validation_error_when_required_credential_field_missing():
    """MESSENGER requires a token; an empty credentials object fails."""
    with pytest.raises(ValidationError):
        ConversationChannelCredentialsResponse.model_validate(
            [{"channel": "MESSENGER", "static_token": {}}]
        )


def test_response_unknown_channel_is_kept_as_unvalidated_extra_field():
    """An unrecognized channel is not rejected: extra='allow' stores it, unvalidated.

    The extras-snakify hook inserts an underscore before every uppercase
    letter, so "UNKNOWN" ends up as "u_n_k_n_o_w_n" rather than "unknown".
    """
    model = ConversationChannelCredentialsResponse.model_validate(
        [
            {
                "channel": "UNKNOWN",
                "static_bearer": {"token": "my-token"},
            }
        ]
    )

    assert model.sms is None
    dumped = model.model_dump(by_alias=True, exclude_none=True)
    assert "u_n_k_n_o_w_n" in dumped #Solved when pass through is implemented
    assert dumped["u_n_k_n_o_w_n"] == {"token": "my-token"}


def test_response_raises_key_error_when_entry_missing_channel_key():
    """An array entry without a 'channel' key cannot be mapped and blows up."""
    with pytest.raises(KeyError):
        ConversationChannelCredentialsResponse.model_validate(
            [{"static_bearer": {"claimed_identity": "sp-id", "token": "tok"}}]
        )


def test_response_last_entry_wins_on_duplicate_channel():
    """If the array has two entries for the same channel, the last one overwrites the first."""
    model = ConversationChannelCredentialsResponse.model_validate(
        [
            {
                "channel": "SMS",
                "static_bearer": {"claimed_identity": "first", "token": "a"},
            },
            {
                "channel": "SMS",
                "static_bearer": {"claimed_identity": "second", "token": "b"},
            },
        ]
    )

    assert model.sms.claimed_identity == "second"
    assert model.sms.token == "b"
