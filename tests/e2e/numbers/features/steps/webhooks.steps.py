import json
import requests
from behave import given, when, then

SINCH_NUMBERS_CALLBACK_SECRET = "strongPa$$PhraseWith36CharactersMax"


def parse_event(context, response):
    context.headers = response.headers
    context.raw_event = response.text
    return json.loads(context.raw_event)


@given("the Numbers Webhooks handler is available")
def step_webhook_handler_is_available(context):
    context.numbers_webhook = context.sinch.numbers.webhooks(SINCH_NUMBERS_CALLBACK_SECRET)


@when('I send a request to trigger the "{status}" for "{event_type}" event')
def step_send_trigger_event(context, status, event_type):
    endpoint = "succeeded" if status == "success" else "failed"
    response = requests.get(f"http://localhost:3013/webhooks/numbers/provisioning_to_voice_platform/{endpoint}")
    event_json = parse_event(context, response)
    context.event = context.numbers_webhook.parse_event(event_json)


@then('the header of the "{status}" for "{event_type}" event contains a valid signature')
def step_check_valid_signature(context, status, event_type):
    assert context.numbers_webhook.validate_authentication_header(
        context.headers, context.raw_event
    ), "Signature validation failed"


@then('the event describes a "{status}" for "{event_type}" event')
def step_check_event_details(context, status, event_type):
    assert context.event.event_type == event_type
    if status == "success":
        assert context.event.status == "SUCCEEDED"
        assert context.event.failure_code is None
    else:
        assert context.event.status == "FAILED"
        assert context.event.failure_code == "PROVISIONING_TO_VOICE_PLATFORM_FAILED"
