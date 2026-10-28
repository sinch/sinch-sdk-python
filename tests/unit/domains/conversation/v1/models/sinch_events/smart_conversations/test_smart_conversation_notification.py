from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.analysis_result import (
    AnalysisResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.smart_conversation_notification import (
    SmartConversationNotification,
)


def test_smart_conversation_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SmartConversationNotification(
        contact_id="contact-1",
        channel_identity="12015555555",
        channel="RCS",
        message_id="message-1",
        conversation_id="conversation-1",
        analysis_results={"ml_pii_result": [{"message": "Hi", "masked": "Hi"}]},
    )

    assert model.contact_id == "contact-1"
    assert model.channel_identity == "12015555555"
    assert model.channel == "RCS"
    assert model.message_id == "message-1"
    assert model.conversation_id == "conversation-1"
    assert isinstance(model.analysis_results, AnalysisResult)
    assert model.analysis_results.ml_pii_result[0].masked == "Hi"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["channel_identity"] == "12015555555"
    assert alias_dump["channel"] == "RCS"
    assert alias_dump["message_id"] == "message-1"
    assert alias_dump["conversation_id"] == "conversation-1"
    assert alias_dump["analysis_results"] == {
        "ml_pii_result": [{"message": "Hi", "masked": "Hi"}]
    }


def test_smart_conversation_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = SmartConversationNotification()

    assert model.contact_id is None
    assert model.channel_identity is None
    assert model.channel is None
    assert model.message_id is None
    assert model.conversation_id is None
    assert model.analysis_results is None


def test_smart_conversation_notification_expects_unknown_channel_accepted():
    """Test that an unknown channel value is accepted through the StrictStr fallback."""
    model = SmartConversationNotification(channel="CARRIER_PIGEON")

    assert model.channel == "CARRIER_PIGEON"
