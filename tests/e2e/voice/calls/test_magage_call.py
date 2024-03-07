from sinch.domains.voice.models.calls.responses import ManageVoiceCallResponse


def test_manage_call(
    sinch_client_sync,
    conference_call_id
):
    update_call_response = sinch_client_sync.voice.calls.manage_with_call_leg(
        call_id=conference_call_id,
        call_leg="caller",
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
    assert isinstance(update_call_response, ManageVoiceCallResponse)


async def test_manage_call_async(
    sinch_client_async,
    conference_call_id
):
    update_call_response = await sinch_client_async.voice.calls.manage_with_call_leg(
        call_id=conference_call_id,
        call_leg="caller",
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
    assert isinstance(update_call_response, ManageVoiceCallResponse)
