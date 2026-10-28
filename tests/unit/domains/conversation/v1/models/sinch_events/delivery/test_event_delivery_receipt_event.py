import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.delivery.event_delivery_receipt_event import (
    EventDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.event_delivery_report import (
    EventDeliveryReport,
)


def test_event_delivery_receipt_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDeliveryReceiptEvent(
        app_id="app-1",
        project_id="project-1",
        event_delivery_report={
            "event_id": "event-1",
            "status": "DELIVERED",
            "contact_id": "contact-1",
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert isinstance(model.event_delivery_report, EventDeliveryReport)
    assert model.event_delivery_report.event_id == "event-1"
    assert model.event_delivery_report.status == "DELIVERED"
    assert model.event_delivery_report.contact_id == "contact-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["event_delivery_report"] == {
        "event_id": "event-1",
        "status": "DELIVERED",
        "contact_id": "contact-1",
    }


def test_event_delivery_receipt_event_expects_validation_error_for_missing_required():
    """Test that app_id, project_id and event_delivery_report are required."""
    with pytest.raises(ValidationError):
        EventDeliveryReceiptEvent()
