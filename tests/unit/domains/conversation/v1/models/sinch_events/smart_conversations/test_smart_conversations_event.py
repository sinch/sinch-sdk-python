from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.smart_conversation_notification import (
    SmartConversationNotification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.smart_conversations_event import (
    SmartConversationsEvent,
)


def test_smart_conversations_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SmartConversationsEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        smart_conversation_notification={
            "message_id": "message-1",
            "analysis_results": {
                "ml_sentiment_result": [{"message": "Hi", "sentiment": "positive"}]
            },
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.smart_conversation_notification, SmartConversationNotification)
    assert model.smart_conversation_notification.message_id == "message-1"
    assert (
        model.smart_conversation_notification.analysis_results.ml_sentiment_result[0].sentiment
        == "positive"
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["smart_conversation_notification"] == {
        "message_id": "message-1",
        "analysis_results": {
            "ml_sentiment_result": [{"message": "Hi", "sentiment": "positive"}]
        },
    }


def test_smart_conversations_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and smart_conversation_notification are required."""
    with pytest.raises(ValidationError):
        SmartConversationsEvent()
