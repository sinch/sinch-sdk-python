from sinch.domains.voice.models.calls.responses import GetVoiceCallResponse


def test_get_call(
    sinch_client_sync,
    call_id
):
    get_call_response = sinch_client_sync.voice.calls.get(
        call_id=call_id
    )
    assert isinstance(get_call_response, GetVoiceCallResponse)


async def test_get_call_async(
    sinch_client_async,
    call_id
):
    get_call_response = await sinch_client_async.voice.calls.get(
        call_id=call_id
    )
    assert isinstance(get_call_response, GetVoiceCallResponse)
