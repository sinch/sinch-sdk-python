import pytest
from pydantic import ValidationError
from sinch.domains.numbers.sinch_events.v1.events import ActiveNumberSinchEvent
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)


def test_active_number_sinch_event_expects_parsed_data():
    """
    Expects all fields to map correctly.
    """
    data = {
        "eventId": "event-123",
        "projectId": "project-456",
        "resourceId": "+1234567890",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_VOICE_PLATFORM",
        "status": "SUCCEEDED",
        "failureCode": "CAMPAIGN_EXPIRED",
        "internalFailureCode": "CRS0018",
    }
    event = ActiveNumberSinchEvent(**data)

    assert isinstance(event, NumberSinchEvent)
    assert event.event_id == "event-123"
    assert event.project_id == "project-456"
    assert event.resource_id == "+1234567890"
    assert event.resource_type == "ACTIVE_NUMBER"
    assert event.event_type == "PROVISIONING_TO_VOICE_PLATFORM"
    assert event.status == "SUCCEEDED"
    assert event.failure_code == "CAMPAIGN_EXPIRED"
    assert event.internal_failure_code == "CRS0018"


def test_active_number_sinch_event_resource_type_defaults_to_active_number():
    """
    Expects resource_type to default to ACTIVE_NUMBER when not provided.
    """
    event = ActiveNumberSinchEvent()

    assert event.resource_type == "ACTIVE_NUMBER"


def test_active_number_sinch_event_missing_optional_fields_expects_parsed_data():
    """
    Expects the model to handle missing optional fields.
    """
    data = {"eventId": "event-123"}
    event = ActiveNumberSinchEvent(**data)

    assert event.event_id == "event-123"
    assert event.event_type is None
    assert event.status is None
    assert event.failure_code is None
    assert event.internal_failure_code is None


def test_active_number_sinch_event_response_invalid_data_expects_validation_error():
    """
    Expects the model to raise a validation error for invalid data.
    """
    data = {"eventId": 123}
    with pytest.raises(ValidationError):
        ActiveNumberSinchEvent(**data)
