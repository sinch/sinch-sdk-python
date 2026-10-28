from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_error_details import (
    OptErrorDetails,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_in_notification import (
    OptInNotification,
)


def test_opt_in_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OptInNotification(
        request_id="request-1",
        contact_id="contact-1",
        channel="WHATSAPP",
        identity="12015555555",
        status="OPT_IN_FAILED",
        error_details={"description": "Rejected"},
        processing_mode="CONVERSATION",
    )

    assert model.request_id == "request-1"
    assert model.contact_id == "contact-1"
    assert model.channel == "WHATSAPP"
    assert model.identity == "12015555555"
    assert model.status == "OPT_IN_FAILED"
    assert isinstance(model.error_details, OptErrorDetails)
    assert model.error_details.description == "Rejected"
    assert model.processing_mode == "CONVERSATION"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["request_id"] == "request-1"
    assert alias_dump["contact_id"] == "contact-1"
    assert alias_dump["channel"] == "WHATSAPP"
    assert alias_dump["identity"] == "12015555555"
    assert alias_dump["status"] == "OPT_IN_FAILED"
    assert alias_dump["error_details"] == {"description": "Rejected"}
    assert alias_dump["processing_mode"] == "CONVERSATION"


def test_opt_in_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = OptInNotification()

    assert model.request_id is None
    assert model.contact_id is None
    assert model.channel is None
    assert model.identity is None
    assert model.status is None
    assert model.error_details is None
    assert model.processing_mode is None