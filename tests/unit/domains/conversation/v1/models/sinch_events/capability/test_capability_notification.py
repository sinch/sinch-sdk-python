from sinch.domains.conversation.models.v1.messages.shared.reason import (
    Reason,
)
from sinch.domains.conversation.models.v1.sinch_events.capability.capability_notification import (
    CapabilityNotification,
)


def test_capability_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CapabilityNotification(
        request_id="request-1",
        contact_id="contact-1",
        channel="RCS",
        identity="12015555555",
        capability_status="CAPABILITY_PARTIAL",
        channel_capabilities=["RICHCARD_STANDALONE", "REVOKE_MESSAGE"],
        reason={"code": "UNKNOWN", "description": "No information"},
    )

    assert model.request_id == "request-1"
    assert model.contact_id == "contact-1"
    assert model.channel == "RCS"
    assert model.identity == "12015555555"
    assert model.capability_status == "CAPABILITY_PARTIAL"
    assert model.channel_capabilities == ["RICHCARD_STANDALONE", "REVOKE_MESSAGE"]
    assert isinstance(model.reason, Reason)
    assert model.reason.code == "UNKNOWN"
    assert model.reason.description == "No information"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["request_id"] == "request-1"
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["channel"] == "RCS"
    assert alias_dump["identity"] == "12015555555"
    assert alias_dump["capability_status"] == "CAPABILITY_PARTIAL"
    assert alias_dump["channel_capabilities"] == [
        "RICHCARD_STANDALONE",
        "REVOKE_MESSAGE",
    ]
    assert alias_dump["reason"] == {
        "code": "UNKNOWN",
        "description": "No information",
    }


def test_capability_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = CapabilityNotification()

    assert model.request_id is None
    assert model.contact_id is None
    assert model.channel is None
    assert model.identity is None
    assert model.capability_status is None
    assert model.channel_capabilities is None
    assert model.reason is None
