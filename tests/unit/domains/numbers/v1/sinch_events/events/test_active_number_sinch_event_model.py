from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.numbers.sinch_events.v1.events.active_number_sinch_event import (
    ActiveNumberSinchEvent,
)


@pytest.fixture
def valid_data():
    return {
        "eventId": "event-123",
        "timestamp": "2025-04-08T09:38:04.854087+00:00",
        "projectId": "project-456",
        "resourceId": "+1234567890",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_SMS_PLATFORM",
        "status": "SUCCEEDED",
        "internalFailureCode": "some-code",
    }


def test_active_number_sinch_event_expects_parsed_data(valid_data):
    event = ActiveNumberSinchEvent(**valid_data)

    assert event.event_id == "event-123"
    assert event.timestamp == datetime(2025, 4, 8, 9, 38, 4, 854087, tzinfo=timezone.utc)
    assert event.project_id == "project-456"
    assert event.resource_id == "+1234567890"
    assert event.resource_type == "ACTIVE_NUMBER"
    assert event.event_type == "PROVISIONING_TO_SMS_PLATFORM"
    assert event.status == "SUCCEEDED"
    assert event.internal_failure_code == "some-code"


def test_active_number_sinch_event_optional_fields_expect_none():
    event = ActiveNumberSinchEvent(resourceType="ACTIVE_NUMBER")

    assert event.event_id is None
    assert event.timestamp is None
    assert event.project_id is None
    assert event.resource_id is None
    assert event.event_type is None
    assert event.status is None
    assert event.internal_failure_code is None


def test_active_number_sinch_event_missing_resource_type_expects_validation_error():
    with pytest.raises(ValidationError):
        ActiveNumberSinchEvent(eventId="event-123")


def test_active_number_sinch_event_invalid_timestamp_expects_validation_error():
    with pytest.raises(ValidationError):
        ActiveNumberSinchEvent(resourceType="ACTIVE_NUMBER", timestamp="not-a-date")
