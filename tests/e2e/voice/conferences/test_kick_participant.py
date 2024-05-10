from sinch.domains.voice.models.conferences.responses import KickParticipantVoiceConferenceResponse


def test_kick_conference_participant(
    sinch_client_sync,
    conference_id,
    conference_call_id
):
    kick_participant_response = sinch_client_sync.voice.conferences.kick_participant(
        conference_id=conference_id,
        call_id=conference_call_id
    )
    assert isinstance(kick_participant_response, KickParticipantVoiceConferenceResponse)


async def test_kick_conference_participant_async(
    sinch_client_async,
    conference_id,
    conference_call_id
):
    kick_participant_response = await sinch_client_async.voice.conferences.kick_participant(
        conference_id=conference_id,
        call_id=conference_call_id
    )
    assert isinstance(kick_participant_response, KickParticipantVoiceConferenceResponse)
