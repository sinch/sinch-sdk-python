import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_base import (  # noqa: E501
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_payload import (  # noqa: E501
    ConversationSinchEventPayload,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_delivery_receipt_event import (  # noqa: E501
    MessageDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_inbound_event import (  # noqa: E501
    MessageInboundEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_submit_event import (  # noqa: E501
    MessageSubmitEvent,
)

adapter = TypeAdapter(ConversationSinchEventPayload)

COMMON = {"app_id": "app-1", "project_id": "project-1"}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {**COMMON, "message_delivery_report": {"status": "DELIVERED"}},
            MessageDeliveryReceiptEvent,
        ),
        (
            {**COMMON, "message": {"id": "m1"}},
            MessageInboundEvent,
        ),
        (
            {**COMMON, "message_submit_notification": {"message_id": "m1"}},
            MessageSubmitEvent,
        ),
        (COMMON, MessageDeliveryReceiptEvent),
        (
            {**COMMON, "reaction_notification": {"emoji": "thumbs_up"}},
            MessageDeliveryReceiptEvent,
        ),
        (
            {**COMMON, "message": "not an object"},
            ConversationSinchEventBase,
        ),
    ],
    ids=[
        "delivery_report",
        "inbound",
        "submit",
        "no_event_payload",
        "unknown_event_payload",
        "invalid_event_payload",
    ],
)
def test_conversation_sinch_event_payload_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each event to resolve from the notification key it carries, an
    event carrying no known key to resolve to the first declared event as it
    always did, and a known key that does not validate to fall back to
    ConversationSinchEventBase.
    """
    with response_parsing_scope():
        event = adapter.validate_python(payload)

    assert type(event) is expected_type
    assert event.app_id == "app-1"
    assert event.project_id == "project-1"
