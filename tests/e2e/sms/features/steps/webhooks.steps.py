import requests
from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.sms.webhooks.v1.sms_webhooks import SmsWebhooks
from sinch.domains.sms.webhooks.v1.events import (
    MOTextWebhookEvent,
)
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)

SINCH_SMS_CALLBACK_SECRET = 'KayakingTheSwell'


def parse_event(context, response):
    context.headers = dict(response.headers)
    context.raw_event = response.text


@given('the SMS Webhooks handler is available')
def step_webhook_handler_is_available(context):
    context.sms_webhook = SmsWebhooks(SINCH_SMS_CALLBACK_SECRET)


@when('I send a request to trigger an "incoming SMS" event')
def step_send_incoming_sms_event(context):
    response = requests.get('http://localhost:3017/webhooks/sms/incoming-sms')
    parse_event(context, response)
    context.event = context.sms_webhook.parse_event(context.raw_event)


@then('the header of the event "{event_type}" contains a valid signature')
@then('the header of the event "{event_type}" with the status "{status}" contains a valid signature')
def step_check_valid_signature(context, event_type, status=None):
    assert context.sms_webhook.validate_authentication_header(
        context.headers, context.raw_event
    ), 'Signature validation failed'


@then('the SMS event describes an "incoming SMS" event')
def step_check_incoming_sms_event(context):
    incoming_sms_event: MOTextWebhookEvent = context.event
    assert incoming_sms_event.id == '01W4FFL35P4NC4K35SMSBATCH8'
    assert incoming_sms_event.from_ == '12015555555'
    assert incoming_sms_event.to == '12017777777'
    assert incoming_sms_event.body == 'Hello John! 👋'
    assert incoming_sms_event.type == 'mo_text'
    assert incoming_sms_event.operator_id == '311071'
    expected_received_at = datetime(2024, 6, 6, 7, 52, 37, 386000, tzinfo=timezone.utc)
    assert incoming_sms_event.received_at == expected_received_at


@when('I send a request to trigger an "SMS delivery report" event')
def step_send_delivery_report_event(context):
    response = requests.get('http://localhost:3017/webhooks/sms/delivery-report-sms')
    parse_event(context, response)
    context.event = context.sms_webhook.parse_event(context.raw_event)


@then('the SMS event describes an "SMS delivery report" event')
def step_check_delivery_report_event(context):
    delivery_report_event: BatchDeliveryReport = context.event
    assert delivery_report_event.batch_id == '01W4FFL35P4NC4K35SMSBATCH8'
    assert delivery_report_event.client_reference == 'client-ref'
    assert delivery_report_event.statuses is not None
    assert len(delivery_report_event.statuses) > 0
    
    status = delivery_report_event.statuses[0]
    assert status.code == 0
    assert status.count == 2
    assert status.status == 'Delivered'
    assert status.recipients is not None
    assert len(status.recipients) == 2
    assert status.recipients[0] == '12017777777'
    assert status.recipients[1] == '33612345678'
    assert delivery_report_event.type == 'delivery_report_sms'


@when('I send a request to trigger an "SMS recipient delivery report" event with the status "Delivered"')
def step_send_recipient_delivery_report_event_delivered(context):
    response = requests.get(
        'http://localhost:3017/webhooks/sms/recipient-delivery-report-sms-delivered'
    )
    parse_event(context, response)
    context.event = context.sms_webhook.parse_event(context.raw_event)


@when('I send a request to trigger an "SMS recipient delivery report" event with the status "Aborted"')
def step_send_recipient_delivery_report_event_aborted(context):
    response = requests.get(
        'http://localhost:3017/webhooks/sms/recipient-delivery-report-sms-aborted'
    )
    parse_event(context, response)
    context.event = context.sms_webhook.parse_event(context.raw_event)


@then('the SMS event describes an SMS recipient delivery report event with the status "Delivered"')
def step_check_recipient_delivery_report_delivered(context):
    recipient_dr_event: RecipientDeliveryReport = context.event
    assert recipient_dr_event.batch_id == '01W4FFL35P4NC4K35SMSBATCH9'
    assert recipient_dr_event.recipient == '12017777777'
    assert recipient_dr_event.code == 0
    assert recipient_dr_event.status == 'Delivered'
    assert recipient_dr_event.type == 'recipient_delivery_report_sms'
    assert recipient_dr_event.client_reference == 'client-ref'
    
    expected_at = datetime(2024, 6, 6, 8, 17, 19, 210000, tzinfo=timezone.utc)
    assert recipient_dr_event.at == expected_at
    
    expected_operator_status_at = datetime(2024, 6, 6, 8, 17, 0, tzinfo=timezone.utc)
    assert recipient_dr_event.operator_status_at == expected_operator_status_at


@then('the SMS event describes an SMS recipient delivery report event with the status "Aborted"')
def step_check_recipient_delivery_report_aborted(context):
    recipient_dr_event: RecipientDeliveryReport = context.event
    assert recipient_dr_event.batch_id == '01W4FFL35P4NC4K35SMSBATCH9'
    assert recipient_dr_event.recipient == '12010000000'
    assert recipient_dr_event.code == 412
    assert recipient_dr_event.status == 'Aborted'
    assert recipient_dr_event.type == 'recipient_delivery_report_sms'
    assert recipient_dr_event.client_reference == 'client-ref'
    
    expected_at = datetime(2024, 6, 6, 8, 17, 15, 603000, tzinfo=timezone.utc)
    assert recipient_dr_event.at == expected_at
