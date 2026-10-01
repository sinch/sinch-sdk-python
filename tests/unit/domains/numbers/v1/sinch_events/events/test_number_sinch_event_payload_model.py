import pytest

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.domains.numbers.sinch_events.v1.events import (
    ActiveNumberSinchEvent,
    NumberOrderSinchEvent,
    NumberSinchEvent,
    NumberSinchEventAdapter,
)


@pytest.mark.parametrize(
    "payload, expected_type, expected_resource_type",
    [
        (
            {
                "eventId": "event-123",
                "resourceType": "ACTIVE_NUMBER",
                "eventType": "PROVISIONING_TO_VOICE_PLATFORM",
                "status": "SUCCEEDED",
            },
            ActiveNumberSinchEvent,
            "ACTIVE_NUMBER",
        ),
        (
            {
                "eventId": "event-123",
                "resourceType": "NUMBER_ORDER",
                "eventType": "NUMBER_ORDER_PROCESSING",
                "status": "IN_REVIEW",
            },
            NumberOrderSinchEvent,
            "NUMBER_ORDER",
        ),
        (
            {
                "eventId": "event-123",
                "resourceType": "SOME_FUTURE_RESOURCE_TYPE",
                "eventType": "SOMETHING_NEW",
            },
            NumberSinchEvent,
            "SOME_FUTURE_RESOURCE_TYPE",
        ),
        ({"eventId": "event-123"}, NumberSinchEvent, None),
    ],
    ids=[
        "active_number",
        "number_order",
        "unknown_resource_type",
        "missing_resource_type",
    ],
)
def test_number_sinch_event_union_resolves_by_resource_type(
    payload, expected_type, expected_resource_type
):
    """
    Expects each resourceType to resolve to its own variant, and both an
    unrecognized and a missing resourceType to fall back to the base
    NumberSinchEvent instead of raising, so resource types added to the API
    later remain parseable.
    """
    with response_parsing_scope():
        event = NumberSinchEventAdapter.validate_python(payload)

    assert type(event) is expected_type
    assert event.event_id == "event-123"
    assert event.resource_type == expected_resource_type
