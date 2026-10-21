import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.message.message_submit_event import (
    MessageSubmitEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.message.message_submit_notification import (
    MessageSubmitNotification,
)


def test_message_submit_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageSubmitEvent(
        app_id="app-1",
        project_id="project-1",
        message_submit_notification={
            "message_id": "message-1",
            "contact_id": "contact-1",
            "submitted_message": {"text_message": {"text": "Hi"}},
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert isinstance(model.message_submit_notification, MessageSubmitNotification)
    assert model.message_submit_notification.message_id == "message-1"
    assert model.message_submit_notification.contact_id == "contact-1"
    assert (
        model.message_submit_notification.submitted_message.text_message.text
        == "Hi"
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["message_submit_notification"] == {
        "message_id": "message-1",
        "contact_id": "contact-1",
        "submitted_message": {"text_message": {"text": "Hi"}},
    }


def test_message_submit_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and message_submit_notification are required."""
    with pytest.raises(ValidationError):
        MessageSubmitEvent()
