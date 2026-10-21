from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.events.shared.app_event import (
    ComposingAppEvent,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.contact_message_event import (
    ReactionContactMessageEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.inbound_event import (
    InboundEvent,
)


def test_inbound_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InboundEvent(
        id="event-1",
        direction="TO_APP",
        contact_event={"composing_event": {}},
        channel_identity={"channel": "MESSENGER", "identity": "123"},
        contact_id="contact-1",
        conversation_id="conversation-1",
        accept_time="2020-11-17T15:09:11Z",
        processing_mode="CONVERSATION",
    )

    assert model.id == "event-1"
    assert model.direction == "TO_APP"
    assert isinstance(model.contact_event, ComposingAppEvent)
    assert model.contact_message_event is None
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "MESSENGER"
    assert model.contact_id == "contact-1"
    assert model.conversation_id == "conversation-1"
    assert model.accept_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert model.processing_mode == "CONVERSATION"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["id"] == "event-1"
    assert alias_dump["direction"] == "TO_APP"
    assert alias_dump["contact_event"] == {"composing_event": {}}
    assert alias_dump["channel_identity"] == {
        "channel": "MESSENGER",
        "identity": "123",
    }
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["conversation_id"] == "conversation-1"
    assert alias_dump["accept_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["processing_mode"] == "CONVERSATION"


def test_inbound_event_expects_contact_message_event_parsed():
    """Test that a contact_message_event is resolved to its variant."""
    model = InboundEvent(
        contact_message_event={
            "reaction_event": {
                "emoji": "thumbs_up",
                "action": "REACTION_ACTION_REACT",
                "message_id": "message-1",
            }
        }
    )

    assert isinstance(model.contact_message_event, ReactionContactMessageEvent)
    assert model.contact_event is None


def test_inbound_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = InboundEvent()

    assert model.id is None
    assert model.direction is None
    assert model.contact_event is None
    assert model.contact_message_event is None
    assert model.channel_identity is None
    assert model.contact_id is None
    assert model.conversation_id is None
    assert model.accept_time is None
    assert model.processing_mode is None
