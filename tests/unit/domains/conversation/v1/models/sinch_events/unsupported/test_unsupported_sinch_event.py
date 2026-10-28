from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.unsupported.unsupported_event import (
    UnsupportedEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.unsupported.unsupported_sinch_event import (
    UnsupportedSinchEvent,
)


def test_unsupported_sinch_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UnsupportedSinchEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        unsupported_callback={"channel": "SMS", "payload": "{}"},
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.unsupported_event, UnsupportedEvent)
    assert model.unsupported_event.channel == "SMS"
    assert model.unsupported_event.payload == "{}"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["unsupported_callback"] == {"channel": "SMS", "payload": "{}"}



def test_unsupported_sinch_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and unsupported_callback are required."""
    with pytest.raises(ValidationError):
        UnsupportedSinchEvent()
