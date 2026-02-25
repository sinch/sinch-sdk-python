import pytest
from datetime import datetime, timezone
from sinch.domains.conversation.models.v1.messages.response import (
    SendMessageResponse,
)


def test_parsing_send_message_response_expects_message_id_only():
    """Test that SendMessageResponse parses with required message_id only."""
    data = {"message_id": "01FC66621XXXXX119Z8PMV1QPQ"}
    parsed = SendMessageResponse.model_validate(data)

    assert isinstance(parsed, SendMessageResponse)
    assert parsed.message_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed.accepted_time is None


def test_parsing_send_message_response_expects_accepted_time():
    """Test that SendMessageResponse parses accepted_time from ISO string."""
    data = {
        "message_id": "01FC66621XXXXX119Z8PMV1QPQ",
        "accepted_time": "2026-01-14T20:32:31.147Z",
    }
    parsed = SendMessageResponse.model_validate(data)

    assert parsed.message_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed.accepted_time == datetime(
        2026, 1, 14, 20, 32, 31, 147000, tzinfo=timezone.utc
    )


def test_send_message_response_expects_message_id_required():
    """Test that SendMessageResponse requires message_id."""
    with pytest.raises(ValueError):
        SendMessageResponse.model_validate({"accepted_time": "2026-01-14T20:32:31.147Z"})
