from sinch.domains.conversation.models.v1.messages.shared.reason import Reason
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.message_delivery_report import (
    MessageDeliveryReport,
)


def test_message_delivery_report_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageDeliveryReport(
        message_id="01EQBC1A3BEK731GY4YXEN0C2R",
        conversation_id="01EPYATA64TMNZ1FV02JKF12JF",
        status="FAILED",
        channel_identity={"channel": "WHATSAPP", "identity": "1234567890"},
        contact_id="01EXA07N79THJ20WSN6AS30TMW",
        metadata="metadata",
        processing_mode="CONVERSATION",
        reason={
            "code": "RECIPIENT_NOT_REACHABLE",
            "description": "Not reachable",
        },
    )

    assert model.message_id == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert model.conversation_id == "01EPYATA64TMNZ1FV02JKF12JF"
    assert model.status == "FAILED"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "WHATSAPP"
    assert model.contact_id == "01EXA07N79THJ20WSN6AS30TMW"
    assert model.metadata == "metadata"
    assert model.processing_mode == "CONVERSATION"
    assert isinstance(model.reason, Reason)
    assert model.reason.code == "RECIPIENT_NOT_REACHABLE"
    assert model.reason.description == "Not reachable"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message_id"] == "01EQBC1A3BEK731GY4YXEN0C2R"
    assert alias_dump["conversation_id"] == "01EPYATA64TMNZ1FV02JKF12JF"
    assert alias_dump["status"] == "FAILED"
    assert alias_dump["channel_identity"] == {
        "channel": "WHATSAPP",
        "identity": "1234567890",
    }
    assert alias_dump["contact_id"] == "01EXA07N79THJ20WSN6AS30TMW"
    assert alias_dump["metadata"] == "metadata"
    assert alias_dump["processing_mode"] == "CONVERSATION"
    assert alias_dump["reason"] == {
        "code": "RECIPIENT_NOT_REACHABLE",
        "description": "Not reachable",
    }


def test_message_delivery_report_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MessageDeliveryReport()

    assert model.message_id is None
    assert model.conversation_id is None
    assert model.status is None
    assert model.channel_identity is None
    assert model.contact_id is None
    assert model.metadata is None
    assert model.processing_mode is None
    assert model.reason is None


def test_message_delivery_report_expects_unknown_status_accepted():
    """Test that an unknown status value is accepted through the StrictStr fallback."""
    model = MessageDeliveryReport(status="TELEPORTED")

    assert model.status == "TELEPORTED"
