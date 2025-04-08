import re
import json
import requests
from behave import given, when, then

SINCH_NUMBERS_CALLBACK_SECRET = 'strongPa$$PhraseWith36CharactersMax'


def parse_event(context, response):
    context.formatted_headers = {k.lower(): v for k, v in response.headers.items()}
    # Strip all whitespace characters from the raw event text.
    raw_event = re.sub(r'\s+', '', response.text)
    context.raw_event = raw_event
    return json.loads(raw_event)


@given('the Numbers Webhooks handler is available')
def step_webhook_handler_is_available(context):
    context.numbers_webhook = context.sinch.numbers.webhooks(SINCH_NUMBERS_CALLBACK_SECRET)


@when('I send a request to trigger the success to provision to voice platform event')
def step_send_trigger_success_event(context):
    response = requests.get('http://localhost:3013/webhooks/numbers/provisioning_to_voice_platform/succeeded')
    event_json = parse_event(context, response)
    context.event = context.numbers_webhook.parse_event(event_json)


@then('the event header contains a valid signature')
def step_check_valid_signature(context):
    assert context.numbers_webhook.validate_authentication_header(
        context.formatted_headers, context.raw_event
    ), "Signature validation failed"


@then('the event describes a success to provision to voice platform event')
def step_check_success_event_details(context):
    assert context.event.event_type == 'PROVISIONING_TO_VOICE_PLATFORM'
    assert context.event.status == 'SUCCEEDED'
    assert context.event.failure_code is None


@when('I send a request to trigger the failure to provision to voice platform event')
def step_send_trigger_failure_event(context):
    response = requests.get('http://localhost:3013/webhooks/numbers/provisioning_to_voice_platform/failed')
    event_json = parse_event(context, response)
    context.event = context.numbers_webhook.parse_event(event_json)


@then('the event describes a failure to provision to voice platform event')
def step_check_failure_event_details(context):
    assert context.event.event_type == 'PROVISIONING_TO_VOICE_PLATFORM'
    assert context.event.status == 'FAILED'
    assert context.event.failure_code == 'PROVISIONING_TO_VOICE_PLATFORM_FAILED'
