from sinch.domains.conversation.models.v1.messages.shared.reason import Reason
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.event_delivery_report import (
    EventDeliveryReport,
)


def test_event_delivery_report_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDeliveryReport(
        event_id="event-1",
        status="FAILED",
        channel_identity={"channel": "SMS", "identity": "+15551234567"},
        contact_id="contact-1",
        reason={"code": "RATE_LIMITED", "description": "Too many events"},
        metadata="metadata",
        processing_mode="DISPATCH",
    )

    assert model.event_id == "event-1"
    assert model.status == "FAILED"
    assert isinstance(model.channel_identity, ChannelIdentity)
    assert model.channel_identity.channel == "SMS"
    assert model.channel_identity.identity == "+15551234567"
    assert model.contact_id == "contact-1"
    assert isinstance(model.reason, Reason)
    assert model.reason.code == "RATE_LIMITED"
    assert model.reason.description == "Too many events"
    assert model.metadata == "metadata"
    assert model.processing_mode == "DISPATCH"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["event_id"] == "event-1"
    assert alias_dump["status"] == "FAILED"
    assert alias_dump["channel_identity"] == {
        "channel": "SMS",
        "identity": "+15551234567",
    }
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["reason"] == {
        "code": "RATE_LIMITED",
        "description": "Too many events",
    }
    assert alias_dump["metadata"] == "metadata"
    assert alias_dump["processing_mode"] == "DISPATCH"


def test_event_delivery_report_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = EventDeliveryReport()

    assert model.event_id is None
    assert model.status is None
    assert model.channel_identity is None
    assert model.contact_id is None
    assert model.reason is None
    assert model.metadata is None
    assert model.processing_mode is None

