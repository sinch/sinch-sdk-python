from sinch.domains.voice.models.calls.responses import UpdateVoiceCallResponse


def test_update_call(
    sinch_client_sync,
    call_id
):
    update_call_response = sinch_client_sync.voice.calls.update(
        call_id=call_id,
        instructions={},
        action={}
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)


async def test_update_call_async(
    sinch_client_async,
    call_id
):
    update_call_response = sinch_client_async.voice.calls.update(
        call_id=call_id
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)
