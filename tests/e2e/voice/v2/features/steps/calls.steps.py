from behave import given, when, then
from sinch.domains.voice.api.v2.calls_apis import Calls
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call

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

@when('I send a request to get call details')
def step_get_call_details(context):
    context.response = context.calls.get(call_id='01HZXK8FQNPMR8VD3JW9YF2C5A')


@then('the response contains the call details')
def step_validate_get_call_details(context):
    data: Call = context.response
    assert data.call_id == '01HZXK8FQNPMR8VD3JW9YF2C5A'
    assert data.project_id == 'a1b2c3d4-e5f6-4789-a012-b3c4d5e6f789'
    assert data.service_id == 'f9e8d7c6-b5a4-4321-9876-c5d4e3f2a1b0'
    assert data.session_id == '01HZXK7QNPMR8VD3JW9YF2C4TB'
    assert data.call_name == 'audio-notification'
    assert data.from_.phone.number == '+12015555555'
    assert data.to.phone.number == '+12017777777'
    assert data.direction == 'OUTBOUND'
    assert data.call_result == 'NO_ANSWER'
    assert data.call_reason == 'NOT_AVAILABLE'
    assert data.call_resource_url == (
        'https://eu1.voice.api.sinch.com/v2/projects/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f789/calls/01HZXK8FQNPMR8VD3JW9YF2C5A'
    )


@when('I send a request to list calls')
def step_list_calls(context):
    context.response = context.calls.list(page_size=2)


@then('the response content contains "{count}" calls')
def step_validate_calls_count(context, count):
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'


@when('I send a request to list all the calls')
def step_list_all_calls(context):
    response = context.calls.list(page_size=2)
    context.calls_list = list(response.iterator())

@then('the calls list contains "{count}" calls')
def step_validate_calls_list_count(context, count):
    expected_count = int(count)
    assert len(context.calls_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.calls_list)}'


@when('I iterate manually over the calls pages')
def step_iterate_manually_calls(context):
    context.list_response = context.calls.list(page_size=2)

    context.calls_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.calls_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the calls iteration result contains the data from "{count}" pages')
def step_validate_calls_pages_count(context, count):
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count}, got {context.pages_iteration}'


@when('I send a request to interact with an ongoing call by call ID')
def step_interact_by_call_id(context):
    context.response = context.calls.interact_by_call_id(
        call_id='01HZXK8FQNPMR8VD3JW9YF2C5A',
        commands=[
            {
                "command": "messages",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "Hello, your call is now connected.",
                            "voice_name": "Emma",
                        },
                    }
                ],
                "events": {"on_finish": [{"command": "hangup"}]},
            }
        ],
    )


@then('the response confirms the interaction request was accepted')
def step_validate_interaction_accepted(context):
    assert context.response is None


@when('I send a request to interact with an ongoing call by call name')
def step_interact_by_call_name(context):
    context.response = context.calls.interact_by_call_name(
        session_id='01HZXK7QNPMR8VD3JW9YF2C4TB',
        call_name='audio-notification',
        commands=[
            {
                "command": "messages",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "Hello, your call is now connected.",
                            "voice_name": "Emma",
                        },
                    }
                ],
                "events": {"on_finish": [{"command": "hangup"}]},
            }
        ],
    )


