from behave import given, when, then
from sinch.domains.voice.api.v2.batches_apis import Batches
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)
from sinch.domains.voice.models.v2.batches.response.start_batch_response import (
    StartBatchResponse,
)

BATCH_ID = "01M144V4N3GSTNVJ3V32TD7H9A"


@given('the Voice-V2 service "Batches" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.batches, Batches), 'Voice-V2 "Batches" service is not available'
    context.batches = context.sinch.voice.v2.batches

@when('I send a request to start a batch of calls')
def step_start_batch_of_calls(context):
    context.response = context.batches.start(
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
    data: StartBatchResponse = context.response
    assert data.batch_id == '01HZXK9RSQNS9WE4KX0ZG3D5UC'
    assert data.project_id == 'b2c3d4e5-f6a7-4890-b123-c4d5e6f7a890'
    assert data.service_id == '0a1b2c3d-4e5f-4678-9abc-d1e2f3a4b5c6'


@when('I send a request to get a batch call summary')
def step_get_batch_call_summary(context):
    context.response = context.batches.get(batch_id=BATCH_ID)


@then('the response contains the batch call summary')
def step_validate_batch_call_summary(context):
    data: BatchSummaryResponse = context.response
    assert data.batch_id == BATCH_ID
    assert data.session_count == 2
    assert data.queued == 0
    assert data.in_progress == 0
    assert data.completed == 2
    assert data.expired == 0
    assert data.ttl_seconds == 1800
    assert data.requested_cps == 5


@when('I send a request to get batch call details')
def step_get_batch_call_details(context):
    context.response = context.batches.get_details(batch_id=BATCH_ID)


@then('the response contains the batch call details')
def step_validate_batch_call_details(context):
    data: BatchDetailsResponse = context.response
    assert len(data.sessions) == 2
    assert data.sessions[0].id == '01M144V4PE5KTSVY2AX19QC332'
    assert data.sessions[0].state == 'IN_PROGRESS'
    assert data.sessions[1].id == '01M144V4PEH22EHB1SHMJRXBXA'
    assert data.sessions[1].state == 'COMPLETED'


@when('I send a request to stop batch processing')
def step_stop_batch_processing(context):
    context.response = context.batches.stop(batch_id=BATCH_ID)


@then('the response confirms the batch stop request was accepted')
def step_validate_stop_batch_processing(context):
    assert context.response is None
