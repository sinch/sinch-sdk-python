from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.shared.app_event import (
    GenericAppEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.event_inbound_event import (
    EventInboundEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.inbound_event import (
    InboundEvent,
)


def test_event_inbound_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventInboundEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        event={
            "id": "event-1",
            "contact_id": "contact-1",
            "contact_event": {"generic_event": {"payload": {"a": 1}}},
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.event, InboundEvent)
    assert model.event.id == "event-1"
    assert model.event.contact_id == "contact-1"
    assert isinstance(model.event.contact_event, GenericAppEvent)
    assert model.event.contact_event.generic_event.payload == {"a": 1}

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["event"] == {
        "id": "event-1",
        "contact_id": "contact-1",
        "contact_event": {"generic_event": {"payload": {"a": 1}}},
    }


def test_event_inbound_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and event are required."""
    with pytest.raises(ValidationError):
        EventInboundEvent()
