from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.numbers.sinch_events.v1.events.number_order_sinch_event import (
    NumberOrderSinchEvent,
)


@pytest.fixture
def valid_data():
    return {
        "eventId": "event-456",
        "timestamp": "2025-04-08T09:38:04.854087+00:00",
        "projectId": "project-456",
        "resourceId": "+1234567890",
        "resourceType": "NUMBER_ORDER",
        "eventType": "NUMBER_ORDER_PROCESSING",
        "status": "COMPLETED",
    }


def test_number_order_sinch_event_expects_parsed_data(valid_data):
    event = NumberOrderSinchEvent(**valid_data)

    assert event.event_id == "event-456"
    assert event.timestamp == datetime(2025, 4, 8, 9, 38, 4, 854087, tzinfo=timezone.utc)
    assert event.project_id == "project-456"
    assert event.resource_id == "+1234567890"
    assert event.resource_type == "NUMBER_ORDER"
    assert event.event_type == "NUMBER_ORDER_PROCESSING"
    assert event.status == "COMPLETED"


def test_number_order_sinch_event_optional_fields_expect_none():
    event = NumberOrderSinchEvent(resourceType="NUMBER_ORDER")

    assert event.event_id is None
    assert event.timestamp is None
    assert event.project_id is None
    assert event.resource_id is None
    assert event.event_type is None
    assert event.status is None


def test_number_order_sinch_event_missing_resource_type_expects_validation_error():
    with pytest.raises(ValidationError):
        NumberOrderSinchEvent(eventId="event-456")


def test_number_order_sinch_event_invalid_timestamp_expects_validation_error():
    with pytest.raises(ValidationError):
        NumberOrderSinchEvent(resourceType="NUMBER_ORDER", timestamp="not-a-date")
