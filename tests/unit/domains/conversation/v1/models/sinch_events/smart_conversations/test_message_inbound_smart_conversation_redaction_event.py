from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.message.inbound_message import (
    InboundMessage,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.message_inbound_smart_conversation_redaction_event import (
    MessageInboundSmartConversationRedactionEvent,
)


def test_message_inbound_smart_conversation_redaction_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageInboundSmartConversationRedactionEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        message_redaction={
            "id": "message-1",
            "contact_id": "contact-1",
            "contact_message": {"text_message": {"text": "My name is [NAME]"}},
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.message_redaction, InboundMessage)
    assert model.message_redaction.id == "message-1"
    assert model.message_redaction.contact_id == "contact-1"
    assert (
        model.message_redaction.contact_message.text_message.text
        == "My name is [NAME]"
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["message_redaction"] == {
        "id": "message-1",
        "contact_id": "contact-1",
        "contact_message": {"text_message": {"text": "My name is [NAME]"}},
    }


def test_message_inbound_smart_conversation_redaction_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and message_redaction are required."""
    with pytest.raises(ValidationError):
        MessageInboundSmartConversationRedactionEvent()
