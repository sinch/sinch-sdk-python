from sinch.domains.voice.models.calls.responses import UpdateVoiceCallResponse


def test_update_call(
    sinch_client_sync,
    call_id
):
    update_call_response = sinch_client_sync.voice.calls.update(
        call_id=call_id,
        instructions=[
            {
              "name": "sendDtmf",
              "value": "1234#"
            }
        ],
        action={
            "name": "hangup"
        }
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)


async def test_update_call_async(
    sinch_client_async,
    call_id
):
    update_call_response = await sinch_client_async.voice.calls.update(
        call_id=call_id,
        instructions=[
            {
              "name": "sendDtmf",
              "value": "1234#"
            }
        ],
        action={
            "name": "hangup"
        }
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)
