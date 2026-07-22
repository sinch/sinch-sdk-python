from sinch.domains.numbers.sinch_events.v1.events import (
    ActiveNumberSinchEvent,
    NumberOrderSinchEvent,
    NumberSinchEvent,
    NumberSinchEventAdapter,
)


def test_number_sinch_event_union_resolves_active_number_variant():
    """
    Expects a payload with resourceType=ACTIVE_NUMBER to resolve to
    ActiveNumberSinchEvent.
    """
    data = {
        "eventId": "event-123",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_VOICE_PLATFORM",
        "status": "SUCCEEDED",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, ActiveNumberSinchEvent)
    assert event.event_id == "event-123"
    assert event.event_type == "PROVISIONING_TO_VOICE_PLATFORM"
    assert event.status == "SUCCEEDED"


def test_number_sinch_event_union_resolves_number_order_variant():
    """
    Expects a payload with resourceType=NUMBER_ORDER to resolve to
    NumberOrderSinchEvent.
    """
    data = {
        "eventId": "event-123",
        "resourceType": "NUMBER_ORDER",
        "eventType": "NUMBER_ORDER_PROCESSING",
        "status": "IN_REVIEW",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert isinstance(event, NumberOrderSinchEvent)
    assert event.event_id == "event-123"
    assert event.event_type == "NUMBER_ORDER_PROCESSING"
    assert event.status == "IN_REVIEW"


def test_number_sinch_event_union_falls_back_to_base_event_for_unknown_resource_type():
    """
    Expects a payload with an unrecognized resourceType to fall back to the
    base NumberSinchEvent instead of raising a validation error, so unseen
    resource types added to the API remain parseable.
    """
    data = {
        "eventId": "event-123",
        "resourceType": "SOME_FUTURE_RESOURCE_TYPE",
        "eventType": "SOMETHING_NEW",
    }
    event = NumberSinchEventAdapter.validate_python(data)

    assert type(event) is NumberSinchEvent
    assert event.event_id == "event-123"
    assert event.resource_type == "SOME_FUTURE_RESOURCE_TYPE"
    assert event.event_type == "SOMETHING_NEW"


def test_number_sinch_event_union_falls_back_when_resource_type_missing():
    """
    Expects a payload missing resourceType entirely to also fall back to the
    base NumberSinchEvent rather than raising a validation error.
    """
    data = {"eventId": "event-123"}
    event = NumberSinchEventAdapter.validate_python(data)

    assert type(event) is NumberSinchEvent
    assert event.event_id == "event-123"
    assert event.resource_type is None
