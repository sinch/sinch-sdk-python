import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.sinch_events.capability.capability_event import (
    CapabilityEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_in_event import (
    OptInEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_out_event import (
    OptOutEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event import (
    ChannelEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.record.record_notification_event import (
    RecordNotificationEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.unsupported.unsupported_sinch_event import (
    UnsupportedSinchEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_create_event import (
    ContactCreateEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_delete_event import (
    ContactDeleteEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_identities_duplication_event import (
    ContactIdentitiesDuplicationEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_merge_event import (
    ContactMergeEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_update_event import (
    ContactUpdateEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_delete_event import (
    ConversationDeleteEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_start_event import (
    ConversationStartEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_stop_event import (
    ConversationStopEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_payload import (
    ConversationSinchEventPayload,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.event_delivery_receipt_event import (
    EventDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.delivery.message_delivery_receipt_event import (
    MessageDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.event_inbound_event import (
    EventInboundEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.message.message_inbound_event import (
    MessageInboundEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.message.message_submit_event import (
    MessageSubmitEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.smart_conversations_event import (
    SmartConversationsEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.message_inbound_smart_conversation_redaction_event import (
    MessageInboundSmartConversationRedactionEvent,
)

adapter = TypeAdapter(ConversationSinchEventPayload)

COMMON = {"app_id": "app-1", "project_id": "project-1"}

MESSAGE_DELIVERY_REPORT = {"message_delivery_report": {"status": "DELIVERED"}}
MESSAGE = {"message": {"id": "message-1"}}
MESSAGE_SUBMIT_NOTIFICATION = {
    "message_submit_notification": {"message_id": "message-1"}
}
MESSAGE_REDACTION = {"message_redaction": {"id": "message-1"}}
EVENT = {"event": {"id": "event-1"}}
EVENT_DELIVERY_REPORT = {
    "event_delivery_report": {"event_id": "event-1", "status": "DELIVERED"}
}
CONVERSATION_START = {
    "conversation_start_notification": {"conversation": {"id": "conversation-1"}}
}
CONVERSATION_STOP = {
    "conversation_stop_notification": {"conversation": {"id": "conversation-1"}}
}
CONVERSATION_DELETE = {
    "conversation_delete_notification": {"conversation": {"id": "conversation-1"}}
}
CONTACT_CREATE = {"contact_create_notification": {"contact": {"id": "contact-1"}}}
CONTACT_DELETE = {"contact_delete_notification": {"contact": {"id": "contact-1"}}}
CONTACT_UPDATE = {"contact_update_notification": {"contact": {"id": "contact-1"}}}
CONTACT_MERGE = {
    "contact_merge_notification": {
        "preserved_contact": {"id": "contact-2"},
        "deleted_contact": {"id": "contact-1"},
    }
}
CAPABILITY = {"capability_notification": {"capability_status": "CAPABILITY_FULL"}}
OPT_IN = {"opt_in_notification": {"status": "OPT_IN_SUCCEEDED"}}
OPT_OUT = {"opt_out_notification": {"status": "OPT_OUT_SUCCEEDED"}}
CHANNEL_EVENT = {"channel_event_notification": {"channel_event": {"event_type": "QUALITY_RATING_UPDATE"}}}
RECORD_NOTIFICATION = {"record_notification": {"record_status": "EVENT_RECORD_STORED"}}
UNSUPPORTED = {"unsupported_callback": {"channel": "SMS"}}
SMART_CONVERSATIONS = {
    "smart_conversation_notification": {
        "message_id": "message-1",
        "analysis_results": {"ml_pii_result": [{"message": "Hi", "masked": "Hi"}]},
    }
}
CONTACT_IDENTITIES_DUPLICATION = {
    "duplicated_contact_identities_notification": {
        "duplicated_identities": [
            {"channel": "SMS", "contact_ids": ["contact-1", "contact-2"]}
        ]
    }
}


@pytest.mark.parametrize(
    "notification, expected_model",
    [
        (MESSAGE_DELIVERY_REPORT, MessageDeliveryReceiptEvent),
        (MESSAGE, MessageInboundEvent),
        (MESSAGE_SUBMIT_NOTIFICATION, MessageSubmitEvent),
        (MESSAGE_REDACTION, MessageInboundSmartConversationRedactionEvent),
        (EVENT, EventInboundEvent),
        (EVENT_DELIVERY_REPORT, EventDeliveryReceiptEvent),
        (CONVERSATION_START, ConversationStartEvent),
        (CONVERSATION_STOP, ConversationStopEvent),
        (CONVERSATION_DELETE, ConversationDeleteEvent),
        (CONTACT_CREATE, ContactCreateEvent),
        (CONTACT_DELETE, ContactDeleteEvent),
        (CONTACT_UPDATE, ContactUpdateEvent),
        (CONTACT_MERGE, ContactMergeEvent),
        (CONTACT_IDENTITIES_DUPLICATION, ContactIdentitiesDuplicationEvent),
        (CAPABILITY, CapabilityEvent),
        (OPT_IN, OptInEvent),
        (OPT_OUT, OptOutEvent),
        (CHANNEL_EVENT, ChannelEvent),
        (RECORD_NOTIFICATION, RecordNotificationEvent),
        (UNSUPPORTED, UnsupportedSinchEvent),
        (SMART_CONVERSATIONS, SmartConversationsEvent),
    ],
    ids=[
        "message_delivery",
        "message_inbound",
        "message_submit",
        "message_redaction",
        "event_inbound",
        "event_delivery",
        "conversation_start",
        "conversation_stop",
        "conversation_delete",
        "contact_create",
        "contact_delete",
        "contact_update",
        "contact_merge",
        "contact_identities_duplication",
        "capability",
        "opt_in",
        "opt_out",
        "channel_event",
        "record_notification",
        "unsupported",
        "smart_conversations",
    ],
)
def test_conversation_sinch_event_payload_expects_each_variant_resolved(
    notification, expected_model
):
    """Test that each event is resolved from the notification key it carries."""
    event = adapter.validate_python({**COMMON, **notification})

    assert type(event) is expected_model
    assert event.app_id == "app-1"
    assert event.project_id == "project-1"


def test_conversation_sinch_event_payload_expects_base_for_unknown_notification():
    """Test that a payload carrying no known notification key resolves to
    ConversationSinchEventBase, keeping the unknown fields as extras."""
    event = adapter.validate_python(
        {**COMMON, "unknown_notification": {"id": "unknown-1"}}
    )

    assert type(event) is ConversationSinchEventBase
    assert event.app_id == "app-1"
    assert event.project_id == "project-1"
    assert event.model_extra == {"unknown_notification": {"id": "unknown-1"}}


def test_conversation_sinch_event_payload_expects_raw_response_without_required_ids_in_a_response():
    """Test that a payload no event accepts is parsed as SinchRawResponse
    instead of failing the whole event."""
    with response_parsing_scope():
        event = adapter.validate_python(MESSAGE)

    assert isinstance(event, SinchRawResponse)
    assert event.model_dump() == MESSAGE

