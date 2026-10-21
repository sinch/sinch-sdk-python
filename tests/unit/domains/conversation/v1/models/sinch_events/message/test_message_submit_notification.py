from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.message.message_submit_notification import (
    MessageSubmitNotification,
)


def test_message_submit_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageSubmitNotification(
        message_id="message-1",
        conversation_id="conversation-1",
        channel_identity={"channel": "WHATSAPP", "identity": "1234567890"},
        contact_id="contact-1",
        submitted_message={"text_message": {"text": "Hi"}},
        metadata="metadata",
        processing_mode="DISPATCH",
    )

    assert model.message_id == "message-1"
    assert model.conversation_id == "conversation-1"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "WHATSAPP"
    assert model.contact_id == "contact-1"
    assert model.submitted_message.text_message.text == "Hi"
    assert model.metadata == "metadata"
    assert model.processing_mode == "DISPATCH"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message_id"] == "message-1"
    assert alias_dump["conversation_id"] == "conversation-1"
    assert alias_dump["channel_identity"] == {
        "channel": "WHATSAPP",
        "identity": "1234567890",
    }
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["submitted_message"] == {"text_message": {"text": "Hi"}}
    assert alias_dump["metadata"] == "metadata"
    assert alias_dump["processing_mode"] == "DISPATCH"


def test_message_submit_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MessageSubmitNotification()

    assert model.message_id is None
    assert model.conversation_id is None
    assert model.channel_identity is None
    assert model.contact_id is None
    assert model.submitted_message is None
    assert model.metadata is None
    assert model.processing_mode is None


def test_message_submit_notification_expects_unknown_processing_mode_accepted():
    """Test that an unknown processing_mode value is accepted through the StrictStr fallback."""
    model = MessageSubmitNotification(processing_mode="OTHER")

    assert model.processing_mode == "OTHER"
