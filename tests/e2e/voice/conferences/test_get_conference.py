from sinch.domains.voice.models.conferences.responses import GetVoiceConferenceResponse


def test_get_conference(
    sinch_client_sync,
    conference_id
):
    get_conference_response = sinch_client_sync.voice.conferences.get(conference_id)
    assert isinstance(get_conference_response, GetVoiceConferenceResponse)


async def test_get_conference_async(
    sinch_client_async,
    conference_id
):
    get_conference_response = await sinch_client_async.voice.conferences.get(conference_id)
    assert isinstance(get_conference_response, GetVoiceConferenceResponse)
