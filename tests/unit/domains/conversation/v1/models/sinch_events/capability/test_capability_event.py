from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.capability.capability_event import (
    CapabilityEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.capability.capability_notification import (
    CapabilityNotification,
)


def test_capability_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CapabilityEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        capability_notification={"request_id": "request-1", "channel": "RCS", "capability_status": "CAPABILITY_FULL"},
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.capability_notification, CapabilityNotification)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["capability_notification"] == {"request_id": "request-1", "channel": "RCS", "capability_status": "CAPABILITY_FULL"}


def test_capability_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and capability_notification are required."""
    with pytest.raises(ValidationError):
        CapabilityEvent()
