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
