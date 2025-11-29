import pytest
from datetime import datetime, timezone
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    parse_json,
    normalize_iso_timestamp,
)


class TestParseJson:
    def test_parse_json_expects_valid_json_string(self):
        """Test parse_json with a valid JSON string."""
        json_string = '{"key": "value", "number": 123}'
        result = parse_json(json_string)
        assert result == {"key": "value", "number": 123}

    def test_parse_json_expects_invalid_json_raises_value_error(self):
        """Test parse_json with invalid JSON raises ValueError."""
        invalid_json = '{"key": "value"'
        with pytest.raises(ValueError, match="Failed to decode JSON"):
            parse_json(invalid_json)


class TestNormalizeIsoTimestamp:
    def test_normalize_iso_timestamp_expects_zulu_suffix(self):
        """Test normalize_iso_timestamp with Zulu timezone suffix (Z)."""
        timestamp_str = "2025-03-15T14:30:45.123Z"
        result = normalize_iso_timestamp(timestamp_str)
        expected = datetime(2025, 3, 15, 14, 30, 45, 123000, tzinfo=timezone.utc)
        assert result == expected

    def test_normalize_iso_timestamp_expects_without_timezone_suffix(self):
        """Test normalize_iso_timestamp without timezone suffix (assumes UTC)."""
        timestamp_str = "2025-07-22T09:15:33.456"
        result = normalize_iso_timestamp(timestamp_str)
        expected = datetime(2025, 7, 22, 9, 15, 33, 456000, tzinfo=timezone.utc)
        assert result == expected

    def test_normalize_iso_timestamp_expects_trims_microseconds(self):
        """Test normalize_iso_timestamp trims microseconds to 6 digits."""
        timestamp_str = "2025-11-08T16:42:17.789123456+00:00"
        result = normalize_iso_timestamp(timestamp_str)
        expected = datetime(2025, 11, 8, 16, 42, 17, 789123, tzinfo=timezone.utc)
        assert result == expected

    def test_normalize_iso_timestamp_expects_without_microseconds(self):
        """Test normalize_iso_timestamp without microseconds."""
        timestamp_str = "2025-01-31T23:59:00Z"
        result = normalize_iso_timestamp(timestamp_str)
        expected = datetime(2025, 1, 31, 23, 59, 0, 0, tzinfo=timezone.utc)
        assert result == expected

    def test_normalize_iso_timestamp_expects_invalid_format_raises_value_error(self):
        """Test normalize_iso_timestamp with invalid format raises ValueError."""
        invalid_timestamp = "not-a-timestamp"
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            normalize_iso_timestamp(invalid_timestamp)
