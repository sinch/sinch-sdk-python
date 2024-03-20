from sinch.domains.voice.models.conferences.responses import KickAllVoiceConferenceResponse


def test_kick_all_conference_participants(
    sinch_client_sync,
    conference_id
):
    kick_all_participants_response = sinch_client_sync.voice.conferences.kick_all(conference_id)
    assert isinstance(kick_all_participants_response, KickAllVoiceConferenceResponse)


async def test_kick_all_conference_participants_async(
    sinch_client_async,
    conference_id
):
    kick_all_participants_response = await sinch_client_async.voice.conferences.kick_all(conference_id)
    assert isinstance(kick_all_participants_response, KickAllVoiceConferenceResponse)
