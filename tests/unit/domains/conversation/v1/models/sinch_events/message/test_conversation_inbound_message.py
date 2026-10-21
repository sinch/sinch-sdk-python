from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    TextContactMessage,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.message.inbound_message import (
    InboundMessage,
)


def test_inbound_message_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InboundMessage(
        id="01EQBC1A3BEK731GY4YXEN0C2R",
        direction="TO_APP",
        contact_message={"text_message": {"text": "Hello"}},
        channel_identity={
            "channel": "WHATSAPP",
            "identity": "1234567890",
            "app_id": "app-1",
        },
        conversation_id="01EPYATA64TMNZ1FV02JKF12JF",
        contact_id="01EXA07N79THJ20WSN6AS30TMW",
        metadata="metadata",
        accept_time="2020-11-17T15:09:11Z",
        sender_id="sender-1",
        processing_mode="CONVERSATION",
        injected=True,
    )

    assert model.id == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert model.direction == "TO_APP"
    assert isinstance(model.contact_message, TextContactMessage)
    assert model.contact_message.text_message.text == "Hello"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "WHATSAPP"
    assert model.channel_identity.identity == "1234567890"
    assert model.channel_identity.app_id == "app-1"
    assert model.conversation_id == "01EPYATA64TMNZ1FV02JKF12JF"
    assert model.contact_id == "01EXA07N79THJ20WSN6AS30TMW"
    assert model.metadata == "metadata"
    assert model.accept_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert model.sender_id == "sender-1"
    assert model.processing_mode == "CONVERSATION"
    assert model.injected is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["id"] == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert alias_dump["direction"] == "TO_APP"
    assert alias_dump["contact_message"] == {"text_message": {"text": "Hello"}}
    assert alias_dump["channel_identity"] == {
        "channel": "WHATSAPP",
        "identity": "1234567890",
        "app_id": "app-1",
    }
    assert alias_dump["conversation_id"] == "01EPYATA64TMNZ1FV02JKF12JF"
    assert alias_dump["contact_id"] == "01EXA07N79THJ20WSN6AS30TMW"
    assert alias_dump["metadata"] == "metadata"
    assert alias_dump["accept_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["sender_id"] == "sender-1"
    assert alias_dump["processing_mode"] == "CONVERSATION"
    assert alias_dump["injected"] is True


def test_inbound_message_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = InboundMessage()

    assert model.id is None
    assert model.direction is None
    assert model.contact_message is None
    assert model.channel_identity is None
    assert model.conversation_id is None
    assert model.contact_id is None
    assert model.metadata is None
    assert model.accept_time is None
    assert model.sender_id is None
    assert model.processing_mode is None
    assert model.injected is None
