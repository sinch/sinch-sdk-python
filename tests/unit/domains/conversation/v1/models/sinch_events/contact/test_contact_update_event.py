from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.contact.contact_notification import (
    ContactNotification,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_update_event import (
    ContactUpdateEvent,
)


def test_contact_update_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ContactUpdateEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        contact_update_notification={"contact": {"id": "contact-1", "display_name": "Jane"}},
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.contact_update_notification, ContactNotification)
    assert model.contact_update_notification.contact.id == "contact-1"
    assert model.contact_update_notification.contact.display_name == "Jane"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["contact_update_notification"] == {
        "contact": {"id": "contact-1", "display_name": "Jane"}
    }


def test_contact_update_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and contact_update_notification are required."""
    with pytest.raises(ValidationError):
        ContactUpdateEvent()
