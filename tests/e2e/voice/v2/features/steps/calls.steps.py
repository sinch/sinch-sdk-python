from behave import given, when, then
from sinch.domains.voice.api.v2.calls_apis import Calls
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)

@given('the Voice-V2 service "Calls" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.calls, Calls), 'Voice-V2 "Calls" service is not available'
    context.calls = context.sinch.voice.v2.calls


@when('I send a request to start a call')
def step_start_call(context):
    context.response = context.calls.start(
        commands=[
            {
                "command": "dial",
                "call_name": "audio-notification",
                "from_": {"type": "PHONE", "phone": {"number": "+12015555555"}},
                "to": {"type": "PHONE", "phone": {"number": "+12017777777"}},
                "dial_timeout_duration_seconds": 30,
                "max_call_duration_seconds": 300,
                "events": {
                    "on_answer": [
                        {
                            "command": "messages",
                            "messages_name": "notification",
                            "messages": [
                                {
                                    "type": "PLAY",
                                    "play": {"url": "https://samplelib.com/mp3/sample-12s.mp3"},
                                },
                                {
                                    "type": "SAY",
                                    "say": {
                                        "text": "Hello! This is a test notification from Sinch. Your verification code is 4 8 3 7.",
                                        "voice_name": "Emma",
                                    },
                                },
                            ],
                            "events": {"on_finish": [{"command": "hangup"}]},
                        }
                    ]
                },
            }
        ]
    )


@then('the response contains the information about the call started')
def step_validate_start_call(context):
    data: StartCallResponse = context.response
    assert data.session_id == '01HZXK7QNPMR8VD3JW9YF2C4TB'
    assert data.project_id == 'a1b2c3d4-e5f6-4789-a012-b3c4d5e6f789'
    assert data.service_id == 'f9e8d7c6-b5a4-4321-9876-c5d4e3f2a1b0'
    assert data.batch_id is None


@when('I send a request to start a batch of calls')
def step_start_batch_of_calls(context):
    context.response = context.calls.start(
        commands=[
            {
                "command": "dial",
                "call_name": "batch-reminder",
                "from_": {"type": "PHONE", "phone": {"number": "+12015555555"}},
                "to": {"type": "PHONE", "phone": {"number": "@toNumber"}},
                "dial_timeout_duration_seconds": 30,
                "max_call_duration_seconds": 120,
                "events": {
                    "on_answer": [
                        {
                            "command": "messages",
                            "messages": [
                                {
                                    "type": "SAY",
                                    "say": {
                                        "text": "Hello, this is an automated reminder from Sinch. Goodbye.",
                                        "voice_name": "Emma",
                                    },
                                }
                            ],
                            "events": {"on_finish": [{"command": "hangup"}]},
                        }
                    ],
                    "on_hangup": [{"command": "hangup"}],
                },
            }
        ],
        parameters=[
            {"toNumber": "+12017777777"},
            {"toNumber": "+12018888888"},
        ],
        batch_options={"max_cps": 5, "ttl_seconds": 600},
    )


@then('the response contains the information about the batch started')
def step_validate_start_batch(context):
    data: StartCallResponse = context.response
    assert data.batch_id == '01HZXK9RSQNS9WE4KX0ZG3D5UC'
    assert data.project_id == 'b2c3d4e5-f6a7-4890-b123-c4d5e6f7a890'
    assert data.service_id == '0a1b2c3d-4e5f-4678-9abc-d1e2f3a4b5c6'
    assert data.session_id is None
