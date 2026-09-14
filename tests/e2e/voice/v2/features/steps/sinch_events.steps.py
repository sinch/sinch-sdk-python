import requests
from behave import given, when, then

from sinch.domains.voice.api.v2.sinch_events import SinchEvents
from sinch.domains.voice.models.v2.sinch_events import VoiceSinchEventRequest
from tests.e2e.helpers import store_webhook_response
from tests.e2e.shared_config import VOICE_V2_ORIGIN

SERVICE_ID = "serviceKey"
SERVICE_SECRET = "BeIukql3pTKJ8RGL5zo0DA=="

# Sinch method used to sign the events for authentication validation
SIGNED_HTTP_METHOD = "POST"

EVENT_PATHS = {
    "call.incoming": "call/incoming",
    "call.answered": "call/answered",
    "call.webhook.on-answer": "call/webhook/on-answer",
}

# For call.webhook.on-answer the event type should be call.customEvent.on-answer
EXPECTED_EVENT_TYPES = {
    "call.webhook.on-answer": "call.customEvent.on-answer",
}

EXPECTED_CALL_ID = "01HZXK7QNPMR8VD3JW9YF2C4CA"
EXPECTED_SESSION_ID = "01HZXK7QNPMR8VD3JW9YF2C4TB"


@given('the Voice-V2 Webhooks handler is available')
def step_webhooks_handler_is_available(context):
    assert isinstance(context.sinch.voice.v2.sinch_events, SinchEvents), (
        'Voice-V2 "SinchEvents" service is not available'
    )
    context.voice_sinch_events = context.sinch.voice.v2.sinch_events


@when('I send a request to trigger a "{event_type}" event')
def step_trigger_event(context, event_type):
    context.event_path = f"/webhooks/voice-v2/{EVENT_PATHS[event_type]}"
    response = requests.get(f"{VOICE_V2_ORIGIN}{context.event_path}")
    store_webhook_response(context, response)


@then('the header of the "{event_type}" event contains a valid authorization')
def step_check_valid_authorization(context, event_type):
    assert context.voice_sinch_events.validate_authentication_header(
        SIGNED_HTTP_METHOD,
        context.event_path,
        context.webhook_headers,
        context.raw_event,
        SERVICE_ID,
        SERVICE_SECRET,
    ), f'Authorization validation failed for event "{event_type}"'


@then('the Voice-V2 event describes a "{event_type}" event')
def step_check_event_type(context, event_type):
    event: VoiceSinchEventRequest = context.voice_sinch_events.parse_event(context.raw_event)
    expected_event_type = EXPECTED_EVENT_TYPES.get(event_type, event_type)
    assert event.event == expected_event_type, (
        f'Expected event "{expected_event_type}", got "{event.event}"'
    )
    assert event.call.call_id == EXPECTED_CALL_ID, (
        f'Expected call_id "{EXPECTED_CALL_ID}", got "{event.call.call_id}"'
    )
    assert event.call.session_id == EXPECTED_SESSION_ID, (
        f'Expected session_id "{EXPECTED_SESSION_ID}", got "{event.call.session_id}"'
    )


@then('the response to the "{event_type}" event matches the expected call control instructions')
def step_respond_with_call_control_instructions(context, event_type):
    response = context.voice_sinch_events.build_response(
        commands=[
            {
                "command": "messages",
                "messages_name": "from-webhook-server",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "This message came from your local webhook server.",
                            "voice_name": "Emma",
                        },
                    }
                ],
                "events": {"on_finish": [{"command": "hangup"}]},
            }
        ]
    )
    body = context.voice_sinch_events.serialize_response(response)
    confirmation = requests.post(f"{VOICE_V2_ORIGIN}{context.event_path}/confirm", json=body)
    assert confirmation.status_code == 200, (
        f"Expected 200 confirming call control instructions for \"{event_type}\", "
        f"got {confirmation.status_code}: {confirmation.text}"
    )
