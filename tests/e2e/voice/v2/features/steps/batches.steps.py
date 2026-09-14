from behave import given, when, then
from sinch.domains.voice.api.v2.batches_apis import Batches
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)

BATCH_ID = "01M144V4N3GSTNVJ3V32TD7H9A"


@given('the Voice-V2 service "Batches" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.batches, Batches), 'Voice-V2 "Batches" service is not available'
    context.batches = context.sinch.voice.v2.batches


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
