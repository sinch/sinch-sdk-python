from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.delivery.message_delivery_receipt_event import (
    MessageDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.message_delivery_report import (
    MessageDeliveryReport,
)


def test_message_delivery_receipt_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageDeliveryReceiptEvent(
        app_id="app-1",
        project_id="project-1",
        accepted_time="2020-11-17T15:09:11Z",
        message_delivery_report={
            "message_id": "message-1",
            "status": "QUEUED_ON_CHANNEL",
            "contact_id": "contact-1",
        },
    )

    assert model.app_id == "app-1"
    assert model.project_id == "project-1"
    assert model.accepted_time == datetime(
        2020, 11, 17, 15, 9, 11, tzinfo=timezone.utc
    )
    assert isinstance(model.message_delivery_report, MessageDeliveryReport)
    assert model.message_delivery_report.message_id == "message-1"
    assert model.message_delivery_report.status == "QUEUED_ON_CHANNEL"
    assert model.message_delivery_report.contact_id == "contact-1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "app-1"
    assert alias_dump["project_id"] == "project-1"
    assert alias_dump["accepted_time"] == "2020-11-17T15:09:11Z"
    assert alias_dump["message_delivery_report"] == {
        "message_id": "message-1",
        "status": "QUEUED_ON_CHANNEL",
        "contact_id": "contact-1",
    }


def test_message_delivery_receipt_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MessageDeliveryReceiptEvent(
        app_id="app-1",
        project_id="project-1",
        message_delivery_report={"status": "DELIVERED"},
    )

    assert model.accepted_time is None
    assert model.event_time is None
    assert model.message_metadata is None
    assert model.correlation_id is None


def test_message_delivery_receipt_event_expects_validation_error_for_missing_report():
    """Test that message_delivery_report is required."""
    with pytest.raises(ValidationError):
        MessageDeliveryReceiptEvent(app_id="app-1", project_id="project-1")
