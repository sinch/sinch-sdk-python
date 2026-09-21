from typing import Any, Dict, List

from sinch.core.exceptions import ValidationException
from sinch.domains.conversation.models.v1.credentials.types import (
    ConversationChannelCredentialsDict,
)

_CHANNEL_CREDENTIAL_FIELD = {
    "WHATSAPP": "static_bearer",
    "RCS": "static_bearer",
    "SMS": "static_bearer",
    "VIBERBM": "static_bearer",
    "MESSENGER": "static_token",
    "MMS": "mms_credentials",
    "INSTAGRAM": "instagram_credentials",
    "TELEGRAM": "telegram_credentials",
    "KAKAOTALK": "kakaotalk_credentials",
    "KAKAOTALKCHAT": "kakaotalkchat_credentials",
    "WECHAT": "wechat_credentials",
    "APPLEBC": "applebc_credentials",
    "LINE": "line_credentials",
}

_KNOWN_CREDENTIAL_FIELDS = set(_CHANNEL_CREDENTIAL_FIELD.values()) | {
    "line_credentials",
    "line_enterprise_credentials",
}

_LINE_ENTERPRISE_SUBKEY = {
    "LINE_JAPAN": "line_japan",
    "LINE_THAILAND": "line_thailand",
}

_LINE_ENTERPRISE_USER_CHANNEL = {
    sub_key: user_channel
    for user_channel, sub_key in _LINE_ENTERPRISE_SUBKEY.items()
}

_COMMON_FIELDS = ("callback_secret", "credential_ordinal_number")


def map_channel_credentials_dict_to_list(
    channel_credentials: ConversationChannelCredentialsDict,
) -> List[Dict[str, Any]]:
    """Translate the channel-keyed credentials map into the API array form.

    Each ``{channel: value}`` entry becomes a
    ``{"channel": channel, <credential_field>: {...}, <common fields>}`` object,
    matching the ``channel_credentials`` array expected by the Conversation API.
    Common fields are lifted to the entry level; every other field is nested
    inside the credential object.

    :param channel_credentials: Credentials keyed by channel name.
    :returns: A list of channel credential objects for the request body.
    :raises ValueError: If a key is not a supported channel.
    """
    if isinstance(channel_credentials, list):
        raise ValidationException(
            message=("channel_credentials must be a dict, not a list."),
            is_from_server=False,
            response=None,
        )
    result: List[Dict[str, Any]] = []
    for user_channel, value in channel_credentials.items():
        common = {key: value[key] for key in _COMMON_FIELDS if key in value}

        if user_channel in _LINE_ENTERPRISE_SUBKEY:
            wire_channel = "LINE"
            credential_field = "line_enterprise_credentials"
            sub_key = _LINE_ENTERPRISE_SUBKEY[user_channel]
            credentials = {
                sub_key: {
                    key: val
                    for key, val in value.items()
                    if key not in _COMMON_FIELDS and key != "is_default"
                }
            }
            if "is_default" in value:
                credentials["is_default"] = value["is_default"]
        elif user_channel in _CHANNEL_CREDENTIAL_FIELD:
            wire_channel = user_channel
            credential_field = _CHANNEL_CREDENTIAL_FIELD[user_channel]
            credentials = {
                key: val
                for key, val in value.items()
                if key not in _COMMON_FIELDS
            }
        else:
            raise ValueError(f"Unsupported channel: {user_channel!r}")

        result.append(
            {"channel": wire_channel, credential_field: credentials, **common}
        )
    return result


def map_channel_credentials_list_to_dict(
    channel_credentials: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Translate the API array form into the channel-keyed credentials map.

    Inverse of :func:`map_channel_credentials_dict_to_list`. Each
    ``{"channel": channel, <credential_field>: {...}, ...}`` object becomes a
    ``{channel: value}`` entry whose value flattens the credential fields and
    keeps the remaining fields.

    :param channel_credentials: The ``channel_credentials`` array from the API.
    :returns: Credentials keyed by channel name.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for entry in channel_credentials:
        user_channel = entry["channel"]
        value: Dict[str, Any] = {}
        for key, val in entry.items():
            if key == "channel":
                continue
            if key == "line_enterprise_credentials" and isinstance(val, dict):
                for sub_field, sub_val in val.items():
                    if (
                        sub_field in _LINE_ENTERPRISE_USER_CHANNEL
                        and isinstance(sub_val, dict)
                    ):
                        user_channel = _LINE_ENTERPRISE_USER_CHANNEL[sub_field]
                        value.update(sub_val)
                    else:
                        value[sub_field] = sub_val
            elif key in _KNOWN_CREDENTIAL_FIELDS and isinstance(val, dict):
                value.update(val)
            else:
                value[key] = val
        result[user_channel] = value
    return result
