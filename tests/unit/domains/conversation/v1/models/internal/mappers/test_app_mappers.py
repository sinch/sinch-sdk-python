import pytest

from sinch.domains.conversation.models.v1.internal.mappers.app_mappers import (
    map_channel_credentials_dict_to_list,
    map_channel_credentials_list_to_dict,
)


class TestMapChannelCredentialsDictToList:
    def test_maps_bearer_channel_to_static_bearer(self):
        result = map_channel_credentials_dict_to_list(
            {"SMS": {"claimed_identity": "sp", "token": "tk"}}
        )
        assert result == [
            {
                "channel": "SMS",
                "static_bearer": {"claimed_identity": "sp", "token": "tk"},
            }
        ]

    def test_maps_messenger_to_static_token(self):
        result = map_channel_credentials_dict_to_list(
            {"MESSENGER": {"token": "fb"}}
        )
        assert result == [
            {"channel": "MESSENGER", "static_token": {"token": "fb"}}
        ]

    def test_maps_mms_to_mms_credentials(self):
        result = map_channel_credentials_dict_to_list(
            {"MMS": {"account_id": "a", "api_key": "k"}}
        )
        assert result == [
            {
                "channel": "MMS",
                "mms_credentials": {"account_id": "a", "api_key": "k"},
            }
        ]

    def test_maps_line_with_token_to_line_credentials(self):
        result = map_channel_credentials_dict_to_list(
            {"LINE": {"token": "t", "secret": "s"}}
        )
        assert result == [
            {"channel": "LINE", "line_credentials": {"token": "t", "secret": "s"}}
        ]

    def test_maps_line_japan_to_enterprise(self):
        result = map_channel_credentials_dict_to_list(
            {"LINE_JAPAN": {"token": "t", "secret": "s"}}
        )
        assert result == [
            {
                "channel": "LINE",
                "line_enterprise_credentials": {
                    "line_japan": {"token": "t", "secret": "s"}
                },
            }
        ]

    def test_maps_line_thailand_to_enterprise(self):
        result = map_channel_credentials_dict_to_list(
            {"LINE_THAILAND": {"token": "t", "secret": "s"}}
        )
        assert result == [
            {
                "channel": "LINE",
                "line_enterprise_credentials": {
                    "line_thailand": {"token": "t", "secret": "s"}
                },
            }
        ]

    def test_maps_line_japan_lifts_is_default(self):
        result = map_channel_credentials_dict_to_list(
            {"LINE_JAPAN": {"token": "t", "secret": "s", "is_default": True}}
        )
        assert result == [
            {
                "channel": "LINE",
                "line_enterprise_credentials": {
                    "line_japan": {"token": "t", "secret": "s"},
                    "is_default": True,
                },
            }
        ]

    def test_lifts_common_fields_to_entry_level(self):
        result = map_channel_credentials_dict_to_list(
            {
                "SMS": {
                    "claimed_identity": "sp",
                    "token": "tk",
                    "callback_secret": "secret",
                    "credential_ordinal_number": 2,
                }
            }
        )
        assert result == [
            {
                "channel": "SMS",
                "static_bearer": {"claimed_identity": "sp", "token": "tk"},
                "callback_secret": "secret",
                "credential_ordinal_number": 2,
            }
        ]

    def test_nests_unknown_field_inside_credential(self):
        result = map_channel_credentials_dict_to_list(
            {"SMS": {"claimed_identity": "sp", "token": "tk", "extra": "x"}}
        )
        assert result[0]["static_bearer"] == {
            "claimed_identity": "sp",
            "token": "tk",
            "extra": "x",
        }

    def test_maps_multiple_channels_preserving_order(self):
        result = map_channel_credentials_dict_to_list(
            {
                "SMS": {"claimed_identity": "sp", "token": "tk"},
                "INSTAGRAM": {"token": "ig"},
            }
        )
        assert [entry["channel"] for entry in result] == ["SMS", "INSTAGRAM"]

    def test_unsupported_channel_raises_value_error(self):
        with pytest.raises(ValueError, match="Unsupported channel"):
            map_channel_credentials_dict_to_list({"NOPE": {"token": "x"}})



class TestMapChannelCredentialsListToDict:
    def test_flattens_credential_into_value(self):
        result = map_channel_credentials_list_to_dict(
            [
                {
                    "channel": "SMS",
                    "static_bearer": {"claimed_identity": "sp", "token": "tk"},
                }
            ]
        )
        assert result == {"SMS": {"claimed_identity": "sp", "token": "tk"}}

    def test_keeps_common_and_readonly_fields(self):
        result = map_channel_credentials_list_to_dict(
            [
                {
                    "channel": "SMS",
                    "static_bearer": {"claimed_identity": "sp", "token": "tk"},
                    "callback_secret": "secret",
                    "credential_ordinal_number": 1,
                    "state": {"status": "ACTIVE"},
                    "channel_known_id": "kid",
                }
            ]
        )
        assert result == {
            "SMS": {
                "claimed_identity": "sp",
                "token": "tk",
                "callback_secret": "secret",
                "credential_ordinal_number": 1,
                "state": {"status": "ACTIVE"},
                "channel_known_id": "kid",
            }
        }

    def test_flattens_line_japan_enterprise(self):
        result = map_channel_credentials_list_to_dict(
            [
                {
                    "channel": "LINE",
                    "line_enterprise_credentials": {
                        "line_japan": {"token": "t", "secret": "s"},
                        "is_default": True,
                    },
                }
            ]
        )
        assert result == {
            "LINE_JAPAN": {
                "token": "t",
                "secret": "s",
                "is_default": True,
            }
        }

    def test_flattens_line_thailand_enterprise(self):
        result = map_channel_credentials_list_to_dict(
            [
                {
                    "channel": "LINE",
                    "line_enterprise_credentials": {
                        "line_thailand": {"token": "t", "secret": "s"},
                    },
                }
            ]
        )
        assert result == {
            "LINE_THAILAND": {
                "token": "t",
                "secret": "s",
            }
        }

    def test_keys_multiple_entries_by_channel(self):
        result = map_channel_credentials_list_to_dict(
            [
                {"channel": "SMS", "static_bearer": {"token": "a", "claimed_identity": "x"}},
                {"channel": "MESSENGER", "static_token": {"token": "b"}},
            ]
        )
        assert set(result.keys()) == {"SMS", "MESSENGER"}
        assert result["SMS"] == {"token": "a", "claimed_identity": "x"}
        assert result["MESSENGER"] == {"token": "b"}

    def test_unknown_credential_field_kept_nested(self):
        result = map_channel_credentials_list_to_dict(
            [{"channel": "SMS", "future_credentials": {"foo": "bar"}}]
        )
        assert result == {"SMS": {"future_credentials": {"foo": "bar"}}}

    def test_null_credential_field_is_kept_under_its_key(self):
        result = map_channel_credentials_list_to_dict(
            [{"channel": "SMS", "claimed_identity": None}]
        )
        assert result == {"SMS": {"claimed_identity": None}}
