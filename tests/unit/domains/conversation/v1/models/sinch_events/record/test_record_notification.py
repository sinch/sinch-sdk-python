from sinch.domains.conversation.models.v1.messages.shared.reason import (
    Reason,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.record.record_notification import (
    RecordNotification,
)


def test_record_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = RecordNotification(
        entity_id="event-1",
        record_status="EVENT_RECORD_STORED",
        channel_identity={"channel": "SMS", "identity": "12015555555"},
        contact_id="contact-1",
        conversation_id="conversation-1",
        reason={"code": "UNKNOWN", "description": "No information"},
        processing_mode="CONVERSATION",
    )

    assert model.entity_id == "event-1"
    assert model.record_status == "EVENT_RECORD_STORED"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.identity == "12015555555"
    assert model.contact_id == "contact-1"
    assert model.conversation_id == "conversation-1"
    assert isinstance(model.reason, Reason)
    assert model.reason.code == "UNKNOWN"
    assert model.processing_mode == "CONVERSATION"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["entity_id"] == "event-1"
    assert alias_dump["record_status"] == "EVENT_RECORD_STORED"
    assert alias_dump["channel_identity"] == {
        "channel": "SMS",
        "identity": "12015555555",
    }
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["conversation_id"] == "conversation-1"
    assert alias_dump["reason"] == {
        "code": "UNKNOWN",
        "description": "No information",
    }
    assert alias_dump["processing_mode"] == "CONVERSATION"


def test_record_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = RecordNotification()

    assert model.entity_id is None
    assert model.record_status is None
    assert model.channel_identity is None
    assert model.contact_id is None
    assert model.conversation_id is None
    assert model.reason is None
    assert model.processing_mode is None

