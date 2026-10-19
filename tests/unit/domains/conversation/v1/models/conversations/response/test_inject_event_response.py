from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.conversations.response.inject_event_response import (
    InjectEventResponse,
)


def test_inject_event_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InjectEventResponse(
        event_id="01W4FFL35P4NC4K35CONVEVENT1",
        accepted_time="2026-10-09T10:00:00Z",
    )

    assert model.event_id == "01W4FFL35P4NC4K35CONVEVENT1"
    assert model.accepted_time == datetime(
        2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "event_id": "01W4FFL35P4NC4K35CONVEVENT1",
        "accepted_time": "2026-10-09T10:00:00Z",
    }


def test_inject_event_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = InjectEventResponse()

    assert model.event_id is None
    assert model.accepted_time is None
