import pytest
from pydantic import ValidationError
from sinch.domains.numbers.sinch_events.v1.events import NumberOrderSinchEvent
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)


def test_number_order_sinch_event_expects_parsed_data():
    """
    Expects all fields to map correctly
    """
    data = {
        "eventId": "event-123",
        "projectId": "project-456",
        "resourceId": "01jgkbb8xywmz3hhahd76menqf",
        "resourceType": "NUMBER_ORDER",
        "eventType": "NUMBER_ORDER_PROCESSING",
        "status": "IN_REVIEW",
        "failureCode": "CAMPAIGN_EXPIRED",  # Not model field
        "internalFailureCode": "CRS0018",  # Not model field
    }
    event = NumberOrderSinchEvent(**data)

    assert isinstance(event, NumberSinchEvent)
    assert event.event_id == "event-123"
    assert event.project_id == "project-456"
    assert event.resource_id == "01jgkbb8xywmz3hhahd76menqf"
    assert event.resource_type == "NUMBER_ORDER"
    assert event.event_type == "NUMBER_ORDER_PROCESSING"
    assert event.status == "IN_REVIEW"
    assert (
        event.failure_code == "CAMPAIGN_EXPIRED"
    )  # Result of inherit from NumberSinchEvent
    assert (
        event.internal_failure_code == "CRS0018"
    )  # Result of inherit from NumberSinchEvent


def test_number_order_sinch_event_resource_type_defaults_to_number_order():
    """
    Expects resource_type to default to NUMBER_ORDER when not provided.
    """
    event = NumberOrderSinchEvent()

    assert event.resource_type == "NUMBER_ORDER"


def test_number_order_sinch_event_missing_optional_fields_expects_parsed_data():
    """
    Expects the model to handle missing optional fields.
    """
    data = {"eventId": "event-123"}
    event = NumberOrderSinchEvent(**data)

    assert event.event_id == "event-123"
    assert event.event_type is None
    assert event.status is None


def test_number_order_sinch_event_response_invalid_data_expects_validation_error():
    """
    Expects the model to raise a validation error for invalid data.
    """
    data = {"eventId": 123}
    with pytest.raises(ValidationError):
        NumberOrderSinchEvent(**data)
