import pytest

from sinch.domains.numbers.sinch_events.v1.events.active_number_sinch_event import (
    ActiveNumberSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_order_sinch_event import (
    NumberOrderSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event_union import (
    NumberSinchEventAdapter,
)


def test_number_sinch_event_union_active_number_returns_active_number_sinch_event():
    data = {
        "eventId": "event-123",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_SMS_PLATFORM",
        "status": "SUCCEEDED",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, ActiveNumberSinchEvent)
    assert event.resource_type == "ACTIVE_NUMBER"
    assert event.event_id == "event-123"


def test_number_sinch_event_union_number_order_returns_number_order_sinch_event():
    data = {
        "eventId": "event-456",
        "resourceType": "NUMBER_ORDER",
        "eventType": "NUMBER_ORDER_PROCESSING",
        "status": "IN_REVIEW",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, NumberOrderSinchEvent)
    assert event.resource_type == "NUMBER_ORDER"
    assert event.event_id == "event-456"


def test_number_sinch_event_union_unknown_resource_type_returns_number_sinch_event():
    data = {
        "eventId": "event-789",
        "resourceType": "UNKNOWN_TYPE",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, NumberSinchEvent)
    assert event.resource_type == "UNKNOWN_TYPE"
    assert event.event_id == "event-789"


def test_number_sinch_event_union_missing_resource_type_returns_number_sinch_event():
    data = {"eventId": "event-000"}
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, NumberSinchEvent)
    assert event.resource_type is None
