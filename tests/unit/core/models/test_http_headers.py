"""Tests for sinch.core.models.http_headers.HttpHeaders."""

import pytest
import requests

from sinch.core.models.http_headers import HttpHeaders


class TestHttpHeaders:
    def test_lookup_is_case_insensitive(self):
        headers = HttpHeaders({"Content-Type": "application/json"})

        assert headers["content-type"] == "application/json"
        assert headers.get("CONTENT-TYPE") == "application/json"
        assert "content-TYPE" in headers

    def test_missing_header_raises_key_error(self):
        with pytest.raises(KeyError):
            HttpHeaders()["X-Missing"]

    def test_add_keeps_repeated_values_in_order(self):
        headers = HttpHeaders()

        headers.add("Accept", "application/json")
        headers.add("accept", "text/plain")

        assert headers.get_all("ACCEPT") == ["application/json", "text/plain"]

    def test_repeated_values_are_joined_on_read(self):
        headers = HttpHeaders([("Accept", "application/json"), ("Accept", "text/plain")])

        assert headers["Accept"] == "application/json, text/plain"

    def test_set_replaces_every_value_and_keeps_position(self):
        headers = HttpHeaders([("A", "1"), ("B", "2"), ("b", "3"), ("C", "4")])

        headers["B"] = "new"

        assert headers.multi_items() == [("A", "1"), ("B", "new"), ("C", "4")]

    def test_delete_removes_every_value(self):
        headers = HttpHeaders([("A", "1"), ("a", "2"), ("B", "3")])

        del headers["A"]

        assert headers.multi_items() == [("B", "3")]

    def test_delete_missing_header_raises_key_error(self):
        with pytest.raises(KeyError):
            del HttpHeaders()["X-Missing"]

    def test_iteration_yields_each_name_once_in_order(self):
        headers = HttpHeaders([("B", "1"), ("A", "2"), ("b", "3")])

        assert list(headers) == ["B", "A"]
        assert len(headers) == 2

    def test_update_overrides_case_insensitively(self):
        headers = HttpHeaders({"Authorization": "Basic abc"})

        headers.update({"authorization": "Bearer xyz"})

        assert headers.get_all("Authorization") == ["Bearer xyz"]

    def test_copies_another_instance_with_repeated_values(self):
        original = HttpHeaders([("Accept", "a"), ("Accept", "b")])

        assert HttpHeaders(original).multi_items() == original.multi_items()

    def test_accepted_by_requests(self):
        headers = HttpHeaders({"X-Trace": "abc"})

        prepared = requests.Request("GET", "https://api.sinch.com", headers=headers).prepare()

        assert prepared.headers["X-Trace"] == "abc"
