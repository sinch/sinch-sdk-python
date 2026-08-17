import json
import requests
from behave import given, when, then
from tests.e2e.helpers import store_webhook_response

SINCH_NUMBERS_CALLBACK_SECRET = 'strongPa$$PhraseWith36CharactersMax'

WEBHOOK_ENDPOINTS = {
    'success': 'provisioning_to_voice_platform/succeeded',
    'failure': 'provisioning_to_voice_platform/failed',
    'completed': 'number_order_processing',
}

EXPECTED_EVENT = {
    'success': ('SUCCEEDED', None),
    'failure': ('FAILED', 'PROVISIONING_TO_VOICE_PLATFORM_FAILED'),
    'completed': ('COMPLETED', None),
}


@given('the Numbers Webhooks handler is available')
def step_webhook_handler_is_available(context):
    context.numbers_webhook = context.sinch.numbers.sinch_events(SINCH_NUMBERS_CALLBACK_SECRET)


@when('I send a request to trigger the "{status}" for "{event_type}" event')
def step_send_trigger_event(context, status, event_type):
    endpoint = WEBHOOK_ENDPOINTS[status]
    response = requests.get(f'http://localhost:3013/webhooks/numbers/{endpoint}')
    store_webhook_response(context, response)
    event_json = json.loads(context.raw_event)
    context.event = context.numbers_webhook.parse_event(event_json)


@then('the header of the "{status}" for "{event_type}" event contains a valid signature')
def step_check_valid_signature(context, status, event_type):
    assert context.numbers_webhook.validate_authentication_header(
        context.webhook_headers, context.raw_event
    ), 'Signature validation failed'


@then('the event describes a "{status}" for "{event_type}" event')
def step_check_event_details(context, status, event_type):
    expected_status, expected_failure_code = EXPECTED_EVENT[status]
    assert context.event.event_type == event_type
    assert context.event.status == expected_status
    assert context.event.failure_code == expected_failure_code
