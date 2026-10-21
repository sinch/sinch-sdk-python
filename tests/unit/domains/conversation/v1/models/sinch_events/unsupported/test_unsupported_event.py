from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.unsupported.unsupported_event import (
    UnsupportedEvent,
)


def test_unsupported_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UnsupportedEvent(
        channel="SMS",
        payload='{"raw": "value"}',
        processing_mode="DISPATCH",
        id="message-1",
        contact_id="contact-1",
        conversation_id="conversation-1",
        channel_identity={"channel": "SMS", "identity": "12015555555"},
    )

    assert model.channel == "SMS"
    assert model.payload == '{"raw": "value"}'
    assert model.processing_mode == "DISPATCH"
    assert model.id == "message-1"
    assert model.contact_id == "contact-1"
    assert model.conversation_id == "conversation-1"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.identity == "12015555555"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["channel"] == "SMS"
    assert alias_dump["payload"] == '{"raw": "value"}'
    assert alias_dump["processing_mode"] == "DISPATCH"
    assert alias_dump["id"] == "message-1"
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["conversation_id"] == "conversation-1"
    assert alias_dump["channel_identity"] == {
        "channel": "SMS",
        "identity": "12015555555",
    }


def test_unsupported_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = UnsupportedEvent()

    assert model.channel is None
    assert model.payload is None
    assert model.processing_mode is None
    assert model.id is None
    assert model.contact_id is None
    assert model.conversation_id is None
    assert model.channel_identity is None
