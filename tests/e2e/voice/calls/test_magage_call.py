from sinch.domains.voice.models.calls.responses import ManageVoiceCallResponse
from sinch.domains.voice.models.svaml.actions import HangupAction
from sinch.domains.voice.models.svaml.instructions import SendDtmfInstruction


def test_manage_call(
    sinch_client_sync,
    conference_call_id
):
    update_call_response = sinch_client_sync.voice.calls.manage_with_call_leg(
        call_id=conference_call_id,
        call_leg="caller",
        instructions=[
            SendDtmfInstruction(
                value="1234#"
            ).as_dict()
        ],
        action=HangupAction().as_dict()
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
            SendDtmfInstruction(
                value="1234#"
            ).as_dict()
        ],
        action=HangupAction().as_dict()
    )
    assert isinstance(update_call_response, ManageVoiceCallResponse)
