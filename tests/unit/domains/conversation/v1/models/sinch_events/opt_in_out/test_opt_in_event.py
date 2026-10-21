from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_in_event import (
    OptInEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_in_notification import (
    OptInNotification,
)


def test_opt_in_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OptInEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        opt_in_notification={"request_id": "request-1", "status": "OPT_IN_SUCCEEDED"},
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.opt_in_notification, OptInNotification)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["opt_in_notification"] == {"request_id": "request-1", "status": "OPT_IN_SUCCEEDED"}


def test_opt_in_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and opt_in_notification are required."""
    with pytest.raises(ValidationError):
        OptInEvent()
