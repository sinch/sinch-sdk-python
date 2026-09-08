from behave import given, when, then
from sinch.domains.voice.api.v2.sessions_apis import Sessions
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)

SESSION_ID = "01J7K3X9M2P5R8V0W4Y6Z1A3B5"


@given('the Voice-V2 service "Sessions" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.sessions, Sessions), 'Voice-V2 "Sessions" service is not available'
    context.sessions = context.sinch.voice.v2.sessions


@when('I send a request to get a session')
def step_get_session(context):
    context.response = context.sessions.get(session_id=SESSION_ID)


@then('the response contains the session details')
def step_validate_session(context):
    data: SessionResponse = context.response
    assert data.session_id == SESSION_ID
    assert data.service_id == 'e52d19b4-03fa-4e89-a901-d78b12f6a9e2'
    assert data.project_id == 'a8f3b91c-4e2d-4190-883a-71b5c92e31d4'
    assert data.state == 'COMPLETED'
    assert len(data.calls) == 1
    call = data.calls[0]
    assert call.call_id == '01J7K3Y2N4Q6S9W1X5Z7A2B4C6'
    assert call.session_id == SESSION_ID
    assert call.batch_id == '01J7K3Z5P6R8T0X2Y7A9B3C5D7'
    assert call.from_.phone.number == '+12015555555'
    assert call.to.phone.number == '+12017777777'
    assert call.direction == 'OUTBOUND'
    assert call.call_result == 'NO_ANSWER'
    assert call.call_reason == 'NOT_AVAILABLE'
