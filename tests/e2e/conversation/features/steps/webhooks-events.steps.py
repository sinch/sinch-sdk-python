import requests
from behave import given, when, then
from sinch.domains.conversation.sinch_events.v1 import ConversationSinchEvent
from sinch.domains.conversation.models.v1.sinch_events import (
    CapabilityEvent,
    ContactCreateEvent,
    ContactDeleteEvent,
    ContactMergeEvent,
    ContactUpdateEvent,
    ConversationDeleteEvent,
    ConversationStartEvent,
    ConversationStopEvent,
    EventDeliveryReceiptEvent,
    EventInboundEvent,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageInboundSmartConversationRedactionEvent,
    MessageSubmitEvent,
    SmartConversationsEvent,
)
from tests.e2e.helpers import has_key_or_attr, store_webhook_response


APP_SECRET = "CactusKnight_SurfsWaves"


def process_event(context, response):
    store_webhook_response(context, response)
    context.event = context.conversation_sinch_events.parse_event(context.raw_event)


def _fetch_and_process(context, path_suffix):
    base_url = context.sinch.configuration.conversation_origin
    url = f"{base_url}/webhooks/conversation/{path_suffix}"
    response = requests.get(url)
    process_event(context, response)


@given("the Conversation Webhooks handler is available")
def step_conversation_webhooks_available(context):
    context.conversation_sinch_events = ConversationSinchEvent(APP_SECRET)


# --- CAPABILITY ---
@when('I send a request to trigger a "CAPABILITY" event')
def step_trigger_capability(context):
    _fetch_and_process(context, "capability-lookup")


# TODO: Refactor to parameterized step to avoid duplication.
@then('the header of the Conversation event "CAPABILITY" contains a valid signature')
def step_signature_valid_capability(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CAPABILITY"


@then('the Conversation event describes a "CAPABILITY" event type')
def step_describes_capability_event_type(context):
    event = context.event
    assert isinstance(event, CapabilityEvent), (
        f"Expected CapabilityEvent, got {type(event)}"
    )
    notification = event.capability_notification
    assert notification is not None, "capability_notification must be present"
    assert notification.capability_status == "CAPABILITY_PARTIAL", (
        f"Unexpected capability_status: {notification.capability_status!r}"
    )


# --- CONTACT_CREATE ---
@when('I send a request to trigger a "CONTACT_CREATE" event')
def step_trigger_contact_create(context):
    _fetch_and_process(context, "contact-create")


@then('the header of the Conversation event "CONTACT_CREATE" contains a valid signature')
def step_signature_valid_contact_create(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONTACT_CREATE"


@then('the Conversation event describes a "CONTACT_CREATE" event type')
def step_describes_contact_create_event_type(context):
    event = context.event
    assert isinstance(event, ContactCreateEvent), (
        f"Expected ContactCreateEvent, got {type(event)}"
    )
    notification = event.contact_create_notification
    assert notification is not None, "contact_create_notification must be present"
    assert notification.contact is not None, "contact must be present"
    assert notification.contact.id == "01W4FFL35P4NC4K35CONTACT01", (
        f"Unexpected contact.id: {notification.contact.id!r}"
    )


# --- CONTACT_DELETE ---
@when('I send a request to trigger a "CONTACT_DELETE" event')
def step_trigger_contact_delete(context):
    _fetch_and_process(context, "contact-delete")


@then('the header of the Conversation event "CONTACT_DELETE" contains a valid signature')
def step_signature_valid_contact_delete(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONTACT_DELETE"


@then('the Conversation event describes a "CONTACT_DELETE" event type')
def step_describes_contact_delete_event_type(context):
    event = context.event
    assert isinstance(event, ContactDeleteEvent), (
        f"Expected ContactDeleteEvent, got {type(event)}"
    )
    notification = event.contact_delete_notification
    assert notification is not None, "contact_delete_notification must be present"
    assert notification.contact is not None, "contact must be present"


# --- CONTACT_MERGE ---
@when('I send a request to trigger a "CONTACT_MERGE" event')
def step_trigger_contact_merge(context):
    _fetch_and_process(context, "contact-merge")


@then('the header of the Conversation event "CONTACT_MERGE" contains a valid signature')
def step_signature_valid_contact_merge(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONTACT_MERGE"


@then('the Conversation event describes a "CONTACT_MERGE" event type')
def step_describes_contact_merge_event_type(context):
    event = context.event
    assert isinstance(event, ContactMergeEvent), (
        f"Expected ContactMergeEvent, got {type(event)}"
    )
    notification = event.contact_merge_notification
    assert notification is not None, "contact_merge_notification must be present"
    assert notification.preserved_contact is not None, "preserved_contact must be present"
    assert notification.preserved_contact.id == "01W4FFL35P4NC4K35CONTACT02", (
        f"Unexpected preserved_contact.id: {notification.preserved_contact.id!r}"
    )


# --- CONTACT_UPDATE ---
@when('I send a request to trigger a "CONTACT_UPDATE" event')
def step_trigger_contact_update(context):
    _fetch_and_process(context, "contact-update")


@then('the header of the Conversation event "CONTACT_UPDATE" contains a valid signature')
def step_signature_valid_contact_update(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONTACT_UPDATE"


@then('the Conversation event describes a "CONTACT_UPDATE" event type')
def step_describes_contact_update_event_type(context):
    event = context.event
    assert isinstance(event, ContactUpdateEvent), (
        f"Expected ContactUpdateEvent, got {type(event)}"
    )
    notification = event.contact_update_notification
    assert notification is not None, "contact_update_notification must be present"
    assert notification.contact is not None, "contact must be present"


# --- CONVERSATION_DELETE ---
@when('I send a request to trigger a "CONVERSATION_DELETE" event')
def step_trigger_conversation_delete(context):
    _fetch_and_process(context, "conversation-delete")


@then('the header of the Conversation event "CONVERSATION_DELETE" contains a valid signature')
def step_signature_valid_conversation_delete(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONVERSATION_DELETE"


@then('the Conversation event describes a "CONVERSATION_DELETE" event type')
def step_describes_conversation_delete_event_type(context):
    event = context.event
    assert isinstance(event, ConversationDeleteEvent), (
        f"Expected ConversationDeleteEvent, got {type(event)}"
    )
    notification = event.conversation_delete_notification
    assert notification is not None, "conversation_delete_notification must be present"
    assert notification.conversation is not None, "conversation must be present"


# --- CONVERSATION_START ---
@when('I send a request to trigger a "CONVERSATION_START" event')
def step_trigger_conversation_start(context):
    _fetch_and_process(context, "conversation-start")


@then('the header of the Conversation event "CONVERSATION_START" contains a valid signature')
def step_signature_valid_conversation_start(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONVERSATION_START"


@then('the Conversation event describes a "CONVERSATION_START" event type')
def step_describes_conversation_start_event_type(context):
    event = context.event
    assert isinstance(event, ConversationStartEvent), (
        f"Expected ConversationStartEvent, got {type(event)}"
    )
    notification = event.conversation_start_notification
    assert notification is not None, "conversation_start_notification must be present"
    assert notification.conversation is not None, "conversation must be present"
    assert notification.conversation.id == "01W4FFL35P4NC4K35CONVERS01", (
        f"Unexpected conversation.id: {notification.conversation.id!r}"
    )


# --- CONVERSATION_STOP ---
@when('I send a request to trigger a "CONVERSATION_STOP" event')
def step_trigger_conversation_stop(context):
    _fetch_and_process(context, "conversation-stop")


@then('the header of the Conversation event "CONVERSATION_STOP" contains a valid signature')
def step_signature_valid_conversation_stop(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event CONVERSATION_STOP"


@then('the Conversation event describes a "CONVERSATION_STOP" event type')
def step_describes_conversation_stop_event_type(context):
    event = context.event
    assert isinstance(event, ConversationStopEvent), (
        f"Expected ConversationStopEvent, got {type(event)}"
    )
    notification = event.conversation_stop_notification
    assert notification is not None, "conversation_stop_notification must be present"
    assert notification.conversation is not None, "conversation must be present"


# --- EVENT_DELIVERY (FAILED) ---
@when('I send a request to trigger a "EVENT_DELIVERY" event with a "FAILED" status')
def step_trigger_event_delivery_failed(context):
    _fetch_and_process(context, "event-delivery-report/failed")


@then('the header of the Conversation event "EVENT_DELIVERY" with a "FAILED" status contains a valid signature')
def step_signature_valid_event_delivery_failed(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event EVENT_DELIVERY with status FAILED"


@then('the Conversation event describes a "EVENT_DELIVERY" event type')
def step_describes_event_delivery_event_type(context):
    event = context.event
    assert isinstance(event, EventDeliveryReceiptEvent), (
        f"Expected EventDeliveryReceiptEvent, got {type(event)}"
    )
    assert event.event_delivery_report is not None, "event_delivery_report must be present"


@then("the Conversation event describes a FAILED event delivery status and its reason")
def step_check_failed_event_delivery_reason(context):
    event_delivery_report = context.event.event_delivery_report
    assert event_delivery_report is not None, "event_delivery_report is missing"
    assert event_delivery_report.status == "FAILED", (
        f"Expected status 'FAILED', got {event_delivery_report.status!r}"
    )
    assert event_delivery_report.reason is not None, "reason is missing for FAILED delivery"
    assert event_delivery_report.reason.code == "BAD_REQUEST", (
        f"Expected reason code 'BAD_REQUEST', got {event_delivery_report.reason.code!r}"
    )


# --- EVENT_DELIVERY (DELIVERED) ---
@when('I send a request to trigger a "EVENT_DELIVERY" event with a "DELIVERED" status')
def step_trigger_event_delivery_delivered(context):
    _fetch_and_process(context, "event-delivery-report/succeeded")


@then('the header of the Conversation event "EVENT_DELIVERY" with a "DELIVERED" status contains a valid signature')
def step_signature_valid_event_delivery_delivered(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event EVENT_DELIVERY with status DELIVERED"


# --- EVENT_INBOUND ---
@when('I send a request to trigger a "EVENT_INBOUND" event')
def step_trigger_event_inbound(context):
    _fetch_and_process(context, "event-inbound")


@then('the header of the Conversation event "EVENT_INBOUND" contains a valid signature')
def step_signature_valid_event_inbound(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event EVENT_INBOUND"


@then('the Conversation event describes a "EVENT_INBOUND" event type')
def step_describes_event_inbound_event_type(context):
    event = context.event
    assert isinstance(event, EventInboundEvent), (
        f"Expected EventInboundEvent, got {type(event)}"
    )
    assert event.event is not None, "event must be present"
    assert has_key_or_attr(event.event.contact_event, "composing_event"), (
        "Expected event.contact_event.composing_event to be present"
    )


# --- MESSAGE_DELIVERY (FAILED) ---
@when('I send a request to trigger a "MESSAGE_DELIVERY" event with a "FAILED" status')
def step_trigger_message_delivery_failed(context):
    _fetch_and_process(context, "message-delivery-report/failed")


@then('the header of the Conversation event "MESSAGE_DELIVERY" with a "FAILED" status contains a valid signature')
def step_signature_valid_message_delivery_failed(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_DELIVERY with status FAILED"


@then('the Conversation event describes a "MESSAGE_DELIVERY" event type')
def step_describes_message_delivery_event_type(context):
    event = context.event
    assert isinstance(event, MessageDeliveryReceiptEvent), (
        f"Expected MessageDeliveryReceiptEvent, got {type(event)}"
    )
    assert event.message_delivery_report is not None, "message_delivery_report must be present"


@then("the Conversation event describes a FAILED message delivery status and its reason")
def step_check_failed_message_delivery_reason(context):
    message_delivery_report = context.event.message_delivery_report
    assert message_delivery_report is not None, "message_delivery_report is missing"
    assert message_delivery_report.status == "FAILED", (
        f"Expected status 'FAILED', got {message_delivery_report.status!r}"
    )
    assert message_delivery_report.reason is not None, "reason is missing for FAILED delivery"
    assert message_delivery_report.reason.code == "RECIPIENT_NOT_REACHABLE", (
        f"Expected reason code 'RECIPIENT_NOT_REACHABLE', got {message_delivery_report.reason.code!r}"
    )


# --- MESSAGE_DELIVERY (QUEUED_ON_CHANNEL) ---
@when('I send a request to trigger a "MESSAGE_DELIVERY" event with a "QUEUED_ON_CHANNEL" status')
def step_trigger_message_delivery_queued(context):
    _fetch_and_process(context, "message-delivery-report/succeeded")


@then('the header of the Conversation event "MESSAGE_DELIVERY" with a "QUEUED_ON_CHANNEL" status contains a valid signature')
def step_signature_valid_message_delivery_queued(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_DELIVERY with status QUEUED_ON_CHANNEL"


# --- MESSAGE_INBOUND ---
@when('I send a request to trigger a "MESSAGE_INBOUND" event')
def step_trigger_message_inbound(context):
    _fetch_and_process(context, "message-inbound")


@then('the header of the Conversation event "MESSAGE_INBOUND" contains a valid signature')
def step_signature_valid_message_inbound(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_INBOUND"


@then('the Conversation event describes a "MESSAGE_INBOUND" event type')
def step_describes_message_inbound_event_type(context):
    event = context.event
    assert isinstance(event, MessageInboundEvent), (
        f"Expected MessageInboundEvent, got {type(event)}"
    )
    assert event.message is not None, "message must be present"


# --- MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION ---
@when('I send a request to trigger a "MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION" event')
def step_trigger_message_inbound_smart_conversation_redaction(context):
    _fetch_and_process(context, "message-inbound/smart-conversation-redaction")


@then('the header of the Conversation event "MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION" contains a valid signature')
def step_signature_valid_message_inbound_smart_conversation_redaction(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION"


@then('the Conversation event describes a "MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION" event type')
def step_describes_message_inbound_smart_conversation_redaction_event_type(context):
    event = context.event
    assert isinstance(event, MessageInboundSmartConversationRedactionEvent), (
        f"Expected MessageInboundSmartConversationRedactionEvent, got {type(event)}"
    )
    assert event.message_redaction is not None, "message_redaction must be present"
    assert has_key_or_attr(event.message_redaction.contact_message, "text_message"), (
        "Expected message_redaction.contact_message.text_message to be present"
    )


# --- MESSAGE_SUBMIT (media) ---
@when('I send a request to trigger a "MESSAGE_SUBMIT" event for a "media" message')
def step_trigger_message_submit_media(context):
    _fetch_and_process(context, "message-submit/media")


@then('the header of the Conversation event "MESSAGE_SUBMIT" for a "media" message contains a valid signature')
def step_signature_valid_message_submit_media(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_SUBMIT for media message"


@then('the Conversation event describes a "MESSAGE_SUBMIT" event type for a "media" message')
def step_check_message_submit_media(context):
    message_submit_event = context.event
    assert isinstance(message_submit_event, MessageSubmitEvent), (
        f"Expected MessageSubmitEvent, got {type(message_submit_event)}"
    )
    assert message_submit_event.message_submit_notification is not None
    submitted = message_submit_event.message_submit_notification.submitted_message
    assert has_key_or_attr(submitted, "media_message"), (
        "Expected submitted_message.media_message to be present"
    )


# --- MESSAGE_SUBMIT (text) ---
@when('I send a request to trigger a "MESSAGE_SUBMIT" event for a "text" message')
def step_trigger_message_submit_text(context):
    _fetch_and_process(context, "message-submit/text")


@then('the header of the Conversation event "MESSAGE_SUBMIT" for a "text" message contains a valid signature')
def step_signature_valid_message_submit_text(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event MESSAGE_SUBMIT for text message"


@then('the Conversation event describes a "MESSAGE_SUBMIT" event type for a "text" message')
def step_check_message_submit_text(context):
    message_submit_event = context.event
    assert isinstance(message_submit_event, MessageSubmitEvent), (
        f"Expected MessageSubmitEvent, got {type(message_submit_event)}"
    )
    assert message_submit_event.message_submit_notification is not None
    submitted = message_submit_event.message_submit_notification.submitted_message
    assert has_key_or_attr(submitted, "text_message"), (
        "Expected submitted_message.text_message to be present"
    )


# --- SMART_CONVERSATIONS (media) ---
@when('I send a request to trigger a "SMART_CONVERSATIONS" event for a "media" message')
def step_trigger_smart_conversations_media(context):
    _fetch_and_process(context, "smart-conversations/media")


@then('the header of the Conversation event "SMART_CONVERSATIONS" for a "media" message contains a valid signature')
def step_signature_valid_smart_conversations_media(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event SMART_CONVERSATIONS for media message"


@then('the Conversation event describes a "SMART_CONVERSATIONS" event type for a "media" message')
def step_check_smart_conversations_media(context):
    event = context.event
    assert isinstance(event, SmartConversationsEvent), (
        f"Expected SmartConversationsEvent, got {type(event)}"
    )
    notification = event.smart_conversation_notification
    assert notification is not None, "smart_conversation_notification must be present"
    analysis_results = notification.analysis_results
    assert analysis_results is not None, "analysis_results must be present"
    assert analysis_results.ml_image_recognition_result, (
        "Expected analysis_results.ml_image_recognition_result to be present"
    )
    assert analysis_results.ml_offensive_analysis_result, (
        "Expected analysis_results.ml_offensive_analysis_result to be present"
    )


# --- SMART_CONVERSATIONS (text) ---
@when('I send a request to trigger a "SMART_CONVERSATIONS" event for a "text" message')
def step_trigger_smart_conversations_text(context):
    _fetch_and_process(context, "smart-conversations/text")


@then('the header of the Conversation event "SMART_CONVERSATIONS" for a "text" message contains a valid signature')
def step_signature_valid_smart_conversations_text(context):
    assert context.conversation_sinch_events.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), "Signature validation failed for event SMART_CONVERSATIONS for text message"


@then('the Conversation event describes a "SMART_CONVERSATIONS" event type for a "text" message')
def step_check_smart_conversations_text(context):
    event = context.event
    assert isinstance(event, SmartConversationsEvent), (
        f"Expected SmartConversationsEvent, got {type(event)}"
    )
    notification = event.smart_conversation_notification
    assert notification is not None, "smart_conversation_notification must be present"
    analysis_results = notification.analysis_results
    assert analysis_results is not None, "analysis_results must be present"
    assert analysis_results.ml_sentiment_result, (
        "Expected analysis_results.ml_sentiment_result to be present"
    )
    assert analysis_results.ml_nlu_result, (
        "Expected analysis_results.ml_nlu_result to be present"
    )
    assert analysis_results.ml_pii_result, (
        "Expected analysis_results.ml_pii_result to be present"
    )
