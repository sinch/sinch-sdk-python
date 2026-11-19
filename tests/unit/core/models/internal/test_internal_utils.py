"""Tests for sinch.core.models.internal.utils helpers."""

import pytest
import requests

from sinch.core.models.internal.utils import (
    basic_auth_header,
    encode_query_parameters,
    strip_unset,
)
from sinch.core.sentinel import UNSET


class TestStripUnset:
    def test_unset_keys_are_removed(self):
        assert strip_unset({"name": UNSET, "limit": UNSET}) == {}

    def test_explicit_none_is_kept(self):
        assert strip_unset({"name": None, "limit": UNSET}) == {"name": None}

    def test_provided_values_are_kept(self):
        data = {"name": "My Item", "limit": 10, "enabled": True}

        assert strip_unset(data) == data

    def test_falsy_values_are_kept(self):
        data = {"name": "", "limit": 0, "enabled": False, "channels": []}

        assert strip_unset(data) == data

    def test_empty_dict_returns_empty_dict(self):
        assert strip_unset({}) == {}

    def test_input_dict_is_not_mutated(self):
        data = {"name": UNSET, "limit": 10}

        result = strip_unset(data)

        assert result == {"limit": 10}
        assert data == {"name": UNSET, "limit": 10}
        assert result is not data


class TestEncodeQueryParameters:
    def test_no_params_is_an_empty_string(self):
        assert encode_query_parameters({}) == ""
        assert encode_query_parameters(None) == ""

    def test_includes_the_leading_question_mark(self):
        assert encode_query_parameters({"pageSize": 5}) == "?pageSize=5"

    def test_list_values_are_repeated(self):
        assert encode_query_parameters({"types": ["MOBILE", "LOCAL"]}) == "?types=MOBILE&types=LOCAL"

    def test_none_values_are_omitted(self):
        assert encode_query_parameters({"a": None, "b": [None, "x"]}) == "?b=x"

    def test_only_none_values_is_an_empty_string(self):
        assert encode_query_parameters({"a": None}) == ""

    @pytest.mark.parametrize("params", [
        {"pageSize": 5, "regionCode": "US"},
        {"to": "+46701234567", "text": "hello world & more"},
        {"types": ["MOBILE", "LOCAL"], "capabilities": "SMS,VOICE"},
        {"name": "Ünïcödé", "flag": True, "count": 0},
        {"start_date": "2026-01-01T00:00:00Z", "skip": None},
    ])
    def test_url_matches_requests_params(self, params):
        url = "https://api.sinch.com/v1/test"
        expected = requests.Request("GET", url, params=params).prepare().url

        actual = requests.Request("GET", url + encode_query_parameters(params)).prepare().url

        assert actual == expected


class TestBasicAuthHeader:
    def test_matches_requests_auth(self):
        expected = requests.Request(
            "GET", "https://auth.sinch.com", auth=("key_id", "key_secret")
        ).prepare().headers["Authorization"]

        assert basic_auth_header("key_id", "key_secret") == expected
