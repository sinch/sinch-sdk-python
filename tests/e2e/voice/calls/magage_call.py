import pytest
from sinch.domains.voice.models.calls.responses import ManageVoiceCallResponse


@pytest.mark.skip(reason="Conference endpoints have to be implemented first.")
def test_manage_call(
    sinch_client_sync,
    call_id
):
    update_call_response = sinch_client_sync.voice.calls.manage(
        call_id=call_id,
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
