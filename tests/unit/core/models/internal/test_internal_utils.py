"""Tests for sinch.core.models.internal.utils helpers."""

from sinch.core.models.internal.utils import strip_unset
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
