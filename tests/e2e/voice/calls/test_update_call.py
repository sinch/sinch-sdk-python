from sinch.domains.voice.models.calls.responses import UpdateVoiceCallResponse
from sinch.domains.voice.models.svaml.actions import HangupAction
from sinch.domains.voice.models.svaml.instructions import SendDtmfInstruction


def test_update_voice_call(
    sinch_client_sync,
    call_id
):
    update_call_response = sinch_client_sync.voice.calls.update(
        call_id=call_id,
        instructions=[
            SendDtmfInstruction(
                value="1234#"
            ).as_dict()
        ],
        action=HangupAction().as_dict()
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)


async def test_update_voice_call_async(
    sinch_client_async,
    call_id
):
    update_call_response = await sinch_client_async.voice.calls.update(
        call_id=call_id,
        instructions=[
            SendDtmfInstruction(
                value="1234#"
            ).as_dict()
        ],
        action=HangupAction().as_dict()
    )
    assert isinstance(update_call_response, UpdateVoiceCallResponse)
