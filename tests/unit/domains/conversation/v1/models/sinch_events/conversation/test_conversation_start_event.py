from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_notification import (
    ConversationNotification,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_start_event import (
    ConversationStartEvent,
)


def test_conversation_start_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConversationStartEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        conversation_start_notification={
            "conversation": {"id": "conversation-1", "contact_id": "contact-1"}
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.conversation_start_notification, ConversationNotification)
    assert model.conversation_start_notification.conversation.id == "conversation-1"
    assert model.conversation_start_notification.conversation.contact_id == "contact-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["conversation_start_notification"] == {
        "conversation": {"id": "conversation-1", "contact_id": "contact-1"}
    }


def test_conversation_start_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and conversation_start_notification are required."""
    with pytest.raises(ValidationError):
        ConversationStartEvent()
