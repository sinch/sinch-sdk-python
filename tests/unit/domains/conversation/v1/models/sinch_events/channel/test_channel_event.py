from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event import (
    ChannelEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_notification import (
    ChannelEventNotification,
)


def test_channel_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ChannelEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        channel_event_notification={"channel_event": {"channel": "WHATSAPP", "event_type": "QUALITY_RATING_UPDATE"}},
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.channel_event_notification, ChannelEventNotification)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["channel_event_notification"] == {"channel_event": {"channel": "WHATSAPP", "event_type": "QUALITY_RATING_UPDATE"}}


def test_channel_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and channel_event_notification are required."""
    with pytest.raises(ValidationError):
        ChannelEvent()
