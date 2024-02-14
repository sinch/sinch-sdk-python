from sinch.domains.voice.models.calls.responses import GetCallResponse


def test_get_call(
    sinch_client_sync,
    # call_id
):
    get_call_response = sinch_client_sync.voice.calls.get(
        call_id="7c5160ce-f62c-495b-8012-b0b1379a618c"
    )
    assert isinstance(get_call_response, GetCallResponse)
